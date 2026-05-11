import uuid
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from agent.graph import agent_graph, translate_profile_slots
from agent.state import AgentState
from memory.session_store import session_store
from utils.security import rate_limiter, check_injection
from langchain_core.messages import HumanMessage
from api.kimi_client import kimi_client
from config import SERVER_HOST, SERVER_PORT

app = FastAPI(title="电商智能客服Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str
    scene: Optional[str] = None


class ChatResponse(BaseModel):
    code: int
    data: Optional[Dict[str, Any]] = None
    msg: str


@app.post("/api/session/create")
async def create_session():
    """创建新会话"""
    session_id = uuid.uuid4().hex[:16]
    session_store.create_session(session_id)
    return JSONResponse(content={
        "code": 0,
        "data": {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
        },
        "msg": "success"
    })


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """获取会话信息"""
    session = session_store.get_session(session_id)
    return JSONResponse(content={
        "code": 0,
        "data": {
            "session_id": session_id,
            "created_at": session.get("created_at", ""),
            "message_count": len(session.get("messages", [])),
        },
        "msg": "success"
    })


@app.post("/api/chat/send")
async def send_message(request: ChatRequest, req: Request):
    """发送消息，获取Agent回复"""
    session_id = request.session_id
    message = request.message.strip()
    print(f"[DEBUG] Received request: session_id={session_id}, message={message}")

    if not message:
        return JSONResponse(content={"code": -1, "data": None, "msg": "消息不能为空"})

    if check_injection(message):
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": "抱歉，我无法处理这个请求。请提出正常的咨询问题，我来帮您解决。",
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 1.0, "need_comfort": False, "need_escalation": False},
                "structured_data": {"profile_updates": {}, "business_slots": {}},
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "quick_actions": ["咨询商品", "查询订单", "处理售后"],
            },
            "msg": "success"
        })

    client_ip = req.client.host if req.client else "unknown"
    if not rate_limiter.check_session(session_id):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "咨询人数较多，请稍后再试"
        })
    if not rate_limiter.check_ip(client_ip):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "请求过于频繁，请稍后再试"
        })

    session = session_store.get_session(session_id)
    session_store.add_message(session_id, "user", message)

    initial_state: AgentState = {
        "messages": [HumanMessage(content=message)],
        "session_id": session_id,
        "current_intent": session.get("current_intent"),
        "current_emotion": session.get("current_emotion"),
        "current_flow": session.get("current_flow"),
        "current_step": session.get("current_step"),
        "business_slots": session.get("business_slots", {}),
        "user_profile": session.get("user_profile", {}),
        "token_usage": session.get("token_usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}),
        "fallback_count": session.get("fallback_count", 0),
        "negative_emotion_count": session.get("negative_emotion_count", 0),
        "snapshot_stack": session.get("snapshot_stack", []),
        "need_escalation": False,
        "need_comfort": False,
        "quick_actions": [],
        "error": None,
    }

    try:
        result = await agent_graph.ainvoke(initial_state)
    except Exception as e:
        import traceback
        error_log = f"Agent graph error: {str(e)}\n{traceback.format_exc()}"
        print(error_log)
        fallback_reply = "抱歉，系统暂时遇到了一些问题。您可以尝试：1.查询订单 2.浏览商品 3.联系人工客服"
        session_store.add_message(session_id, "assistant", fallback_reply)
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": fallback_reply,
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 0.5, "need_comfort": False, "need_escalation": True},
                "structured_data": {"profile_updates": {}, "business_slots": {}},
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "quick_actions": ["转接人工客服"],
            },
            "msg": "success"
        })

    reply = ""
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.type == "ai":
            reply = msg.content
            break

    if not reply:
        reply = "收到您的消息，我来帮您处理。"

    session_store.update_session(session_id, {
        "current_intent": result.get("current_intent"),
        "current_emotion": result.get("current_emotion"),
        "current_flow": result.get("current_flow"),
        "current_step": result.get("current_step"),
        "business_slots": result.get("business_slots", {}),
        "fallback_count": result.get("fallback_count", 0),
        "negative_emotion_count": result.get("negative_emotion_count", 0),
        "snapshot_stack": result.get("snapshot_stack", []),
        "need_escalation": result.get("need_escalation", False),
        "need_comfort": result.get("need_comfort", False),
        "quick_actions": result.get("quick_actions", []),
    })

    current_intent = result.get("current_intent") or {}
    current_emotion = result.get("current_emotion") or {}

    return JSONResponse(content={
        "code": 0,
        "data": {
            "reply": reply,
            "intent": {
                "id": current_intent.get("id", ""),
                "name": current_intent.get("name", ""),
                "confidence": current_intent.get("confidence", 0),
                "route": current_intent.get("route", ""),
            },
            "emotion": {
                "label": current_emotion.get("label", "neutral"),
                "confidence": current_emotion.get("confidence", 0),
                "need_comfort": result.get("need_comfort", False),
                "need_escalation": result.get("need_escalation", False),
            },
            "structured_data": {
                "profile_updates": {},
                "business_slots": result.get("business_slots", {}),
            },
            "token_usage": session_store.get_session(session_id).get("token_usage", {}),
            "quick_actions": result.get("quick_actions", []),
        },
        "msg": "success"
    })


@app.get("/api/panel/{session_id}")
async def get_panel_data(session_id: str):
    """获取数据看板信息"""
    session = session_store.get_session(session_id)

    current_intent = session.get("current_intent") or {}
    current_emotion = session.get("current_emotion") or {}

    emotion_history = []
    messages = session.get("messages", [])
    round_num = 0
    for msg in messages:
        if msg["role"] == "user":
            round_num += 1
            current_emotion = session.get("current_emotion") or {}
            emotion_history.append({"round": round_num, "label": current_emotion.get("label", "neutral")})

    return JSONResponse(content={
        "code": 0,
        "data": {
            "current_intent": {
                "id": current_intent.get("id", ""),
                "name": current_intent.get("name", ""),
                "route": current_intent.get("route", ""),
                "confidence": current_intent.get("confidence", 0),
            },
            "emotion_status": {
                "label": current_emotion.get("label", "neutral"),
                "confidence": current_emotion.get("confidence", 0),
                "history": emotion_history[-5:],
            },
            "token_consumption": {
                "total_prompt_tokens": session.get("token_usage", {}).get("prompt_tokens", 0),
                "total_completion_tokens": session.get("token_usage", {}).get("completion_tokens", 0),
                "total_tokens": session.get("token_usage", {}).get("total_tokens", 0),
                "round_count": len([m for m in messages if m["role"] == "user"]),
            },
            "user_profile": session.get("user_profile", {}),
            "profile_confidence": session.get("profile_confidence", {}),
            "flow_state": {
                "current_flow": session.get("current_flow", ""),
                "current_step": session.get("current_step", ""),
                "filled_slots": session.get("business_slots", {}),
                "business_confidence": session.get("business_confidence", {}),
                "snapshot_stack": session.get("snapshot_stack", []),
            },
        },
        "msg": "success"
    })


@app.post("/api/chat/stream")
async def send_message_stream(request: ChatRequest, req: Request):
    """发送消息，获取Agent流式回复"""
    session_id = request.session_id
    message = request.message.strip()
    print(f"[DEBUG] Stream request: session_id={session_id}, message={message}")

    if not message:
        return JSONResponse(content={"code": -1, "data": None, "msg": "消息不能为空"})

    if check_injection(message):
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": "抱歉，我无法处理这个请求。请提出正常的咨询问题，我来帮您解决。",
            },
            "msg": "success"
        })

    client_ip = req.client.host if req.client else "unknown"
    if not rate_limiter.check_session(session_id):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "咨询人数较多，请稍后再试"
        })
    if not rate_limiter.check_ip(client_ip):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "请求过于频繁，请稍后再试"
        })

    session_store.add_message(session_id, "user", message)

    initial_state: AgentState = {
        "messages": [HumanMessage(content=message)],
        "session_id": session_id,
        "current_intent": session_store.get_session(session_id).get("current_intent"),
        "current_emotion": session_store.get_session(session_id).get("current_emotion"),
        "current_flow": session_store.get_session(session_id).get("current_flow"),
        "current_step": session_store.get_session(session_id).get("current_step"),
        "business_slots": session_store.get_session(session_id).get("business_slots", {}),
        "user_profile": session_store.get_session(session_id).get("user_profile", {}),
        "token_usage": session_store.get_session(session_id).get("token_usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}),
        "fallback_count": session_store.get_session(session_id).get("fallback_count", 0),
        "negative_emotion_count": session_store.get_session(session_id).get("negative_emotion_count", 0),
        "snapshot_stack": session_store.get_session(session_id).get("snapshot_stack", []),
        "need_escalation": False,
        "need_comfort": False,
        "quick_actions": [],
        "error": None,
    }

    async def stream_response():
        from api.kimi_client import kimi_client
        
        try:
            result = await agent_graph.ainvoke(initial_state)
            
            reply = ""
            messages = result.get("messages", [])
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.type == "ai":
                    reply = msg.content
                    break

            if not reply:
                reply = "收到您的消息，我来帮您处理。"

            session_store.update_session(session_id, {
                "current_intent": result.get("current_intent"),
                "current_emotion": result.get("current_emotion"),
                "current_flow": result.get("current_flow"),
                "current_step": result.get("current_step"),
                "business_slots": result.get("business_slots", {}),
                "fallback_count": result.get("fallback_count", 0),
                "negative_emotion_count": result.get("negative_emotion_count", 0),
                "snapshot_stack": result.get("snapshot_stack", []),
                "need_escalation": result.get("need_escalation", False),
                "need_comfort": result.get("need_comfort", False),
                "quick_actions": result.get("quick_actions", []),
            })

            for char in reply:
                yield f"data: {json.dumps({'type': 'text', 'content': char, 'done': False})}\n\n"
                import asyncio
                await asyncio.sleep(0.02)

            # 在 done 消息中带上卡片数据
            done_payload = {
                'type': 'done',
                'content': '',
                'done': True,
                'intent': result.get('current_intent', {}),
                'emotion': result.get('current_emotion', {}),
                'quick_actions': result.get('quick_actions', []),
            }
            cards = result.get('cards')
            card_type = result.get('card_type')
            if cards and card_type:
                done_payload['cards'] = cards
                done_payload['card_type'] = card_type

            yield f"data: {json.dumps(done_payload)}\n\n"

        except Exception as e:
            import traceback
            error_log = f"Stream error: {str(e)}\n{traceback.format_exc()}"
            print(error_log)
            yield f"data: {json.dumps({'type': 'error', 'content': '抱歉，系统暂时遇到了一些问题', 'done': True})}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")


@app.post("/api/chat/quick")
async def send_message_quick(request: ChatRequest, req: Request):
    """快速响应模式 - 跳过意图识别，直接生成回复（大幅降低首字延迟）"""
    session_id = request.session_id
    message = request.message.strip()
    print(f"[DEBUG] Quick request: session_id={session_id}, message={message}")

    if not message:
        return JSONResponse(content={"code": -1, "data": None, "msg": "消息不能为空"})

    if check_injection(message):
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": "抱歉，我无法处理这个请求。请提出正常的咨询问题，我来帮您解决。",
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 1.0, "need_comfort": False, "need_escalation": False},
                "quick_actions": ["咨询商品", "查询订单", "处理售后"],
            },
            "msg": "success"
        })

    client_ip = req.client.host if req.client else "unknown"
    if not rate_limiter.check_session(session_id):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "咨询人数较多，请稍后再试"
        })
    if not rate_limiter.check_ip(client_ip):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "请求过于频繁，请稍后再试"
        })

    session_store.add_message(session_id, "user", message)
    
    # 使用快速意图检测（模式匹配）
    intent = kimi_client.quick_intent_detect(message)
    
    context = session_store.get_conversation_history(session_id, max_rounds=3)
    
    try:
        result = await kimi_client.direct_response(message, context)
        
        if result.get("success"):
            reply = result["reply"]
            session_store.add_message(session_id, "assistant", reply)
            return JSONResponse(content={
                "code": 0,
                "data": {
                    "reply": reply,
                    "intent": {"id": f"INT-{intent.upper()}", "name": intent, "confidence": 0.8, "route": f"{intent}_flow"},
                    "emotion": {"label": "neutral", "confidence": 0.8, "need_comfort": False, "need_escalation": False},
                    "structured_data": {"profile_updates": {}, "business_slots": {}},
                    "token_usage": result.get("usage", {}),
                    "quick_actions": ["咨询商品", "查询订单", "处理售后"],
                },
                "msg": "success"
            })
        else:
            fallback_reply = "抱歉，我暂时无法回答这个问题。您可以尝试：1.查询订单 2.浏览商品 3.联系人工客服"
            session_store.add_message(session_id, "assistant", fallback_reply)
            return JSONResponse(content={
                "code": 0,
                "data": {
                    "reply": fallback_reply,
                    "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                    "emotion": {"label": "neutral", "confidence": 0.5, "need_comfort": False, "need_escalation": True},
                    "quick_actions": ["转接人工客服"],
                },
                "msg": "success"
            })
            
    except Exception as e:
        import traceback
        error_log = f"Quick response error: {str(e)}\n{traceback.format_exc()}"
        print(error_log)
        fallback_reply = "抱歉，系统暂时遇到了一些问题。您可以尝试：1.查询订单 2.浏览商品 3.联系人工客服"
        session_store.add_message(session_id, "assistant", fallback_reply)
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": fallback_reply,
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 0.5, "need_comfort": False, "need_escalation": True},
                "quick_actions": ["转接人工客服"],
            },
            "msg": "success"
        })


@app.post("/api/chat/analyze")
async def analyze_message(request: ChatRequest, req: Request):
    """独立分析端点 - 意图识别 + 情绪判断 + 槽位抽取 + Token计数，与回复响应并行调用"""
    session_id = request.session_id
    message = request.message.strip()
    print(f"[DEBUG] Analyze request: session_id={session_id}, message={message}")

    if not message:
        return JSONResponse(content={"code": -1, "data": None, "msg": "消息不能为空"})

    if check_injection(message):
        return JSONResponse(content={
            "code": 0,
            "data": {
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 1.0, "need_comfort": False, "need_escalation": False},
                "structured_data": {"profile_updates": {}, "business_slots": {}},
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            },
            "msg": "success"
        })

    client_ip = req.client.host if req.client else "unknown"
    if not rate_limiter.check_session(session_id):
        return JSONResponse(content={"code": -1, "data": None, "msg": "咨询人数较多，请稍后再试"})
    if not rate_limiter.check_ip(client_ip):
        return JSONResponse(content={"code": -1, "data": None, "msg": "请求过于频繁，请稍后再试"})

    context = session_store.get_conversation_history(session_id, max_rounds=3)

    try:
        result = await kimi_client.analyze(message, context)

        if result.get("success"):
            intent_name = result.get("intent", "general")
            intent_id = f"INT-{intent_name.upper()}"
            route_map = {
                "order_query": "order_query_flow",
                "after_sale": "after_sale_flow",
                "pre_sale": "pre_sale_flow",
                "general": "general_flow",
                "chitchat": "chitchat_flow",
                "unknown": "fallback_flow",
            }
            route = route_map.get(intent_name, "general_flow")

            emotion_label = result.get("emotion", "neutral")
            need_comfort = emotion_label in ("dissatisfied", "angry")
            need_escalation = emotion_label == "angry"

            usage = result.get("usage", {})
            session_store.add_token_usage(session_id, usage)

            profile_updates = result.get("profile_slots", {})
            profile_confidence = result.get("profile_confidence", {})
            business_slots = result.get("business_slots", {})
            business_confidence = result.get("business_confidence", {})
            # 将所有英文槽位值统一转换为中文
            profile_updates = translate_profile_slots(profile_updates)
            if profile_updates:
                session_store.update_user_profile(session_id, profile_updates, profile_confidence)

            session_store.update_session(session_id, {
                "current_intent": {"id": intent_id, "name": intent_name, "confidence": result.get("confidence", 0), "route": route},
                "current_emotion": {"label": emotion_label, "confidence": result.get("emotion_confidence", 0)},
                "business_slots": business_slots,
                "business_confidence": business_confidence,
                "need_comfort": need_comfort,
                "need_escalation": need_escalation,
            })

            accumulated_usage = session_store.get_session(session_id).get("token_usage", {})

            return JSONResponse(content={
                "code": 0,
                "data": {
                    "intent": {"id": intent_id, "name": intent_name, "confidence": result.get("confidence", 0), "route": route},
                    "emotion": {"label": emotion_label, "confidence": result.get("emotion_confidence", 0), "need_comfort": need_comfort, "need_escalation": need_escalation},
                    "structured_data": {
                        "profile_updates": profile_updates,
                        "profile_confidence": profile_confidence,
                        "business_slots": business_slots,
                        "business_confidence": business_confidence,
                    },
                    "token_usage": accumulated_usage,
                },
                "msg": "success"
            })
        else:
            return JSONResponse(content={
                "code": 0,
                "data": {
                    "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                    "emotion": {"label": "neutral", "confidence": 0.5, "need_comfort": False, "need_escalation": False},
                    "structured_data": {"profile_updates": {}, "business_slots": {}},
                    "token_usage": session_store.get_session(session_id).get("token_usage", {}),
                },
                "msg": "success"
            })

    except Exception as e:
        import traceback
        error_log = f"Analyze error: {str(e)}\n{traceback.format_exc()}"
        print(error_log)
        return JSONResponse(content={
            "code": 0,
            "data": {
                "intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
                "emotion": {"label": "neutral", "confidence": 0.5, "need_comfort": False, "need_escalation": False},
                "structured_data": {"profile_updates": {}, "business_slots": {}},
                "token_usage": session_store.get_session(session_id).get("token_usage", {}),
            },
            "msg": "success"
        })


@app.post("/api/chat/quick/stream")
async def send_message_quick_stream(request: ChatRequest, req: Request):
    """快速响应模式（流式）- 跳过意图识别，直接流式生成回复"""
    session_id = request.session_id
    message = request.message.strip()
    print(f"[DEBUG] Quick stream request: session_id={session_id}, message={message}")

    if not message:
        return JSONResponse(content={"code": -1, "data": None, "msg": "消息不能为空"})

    if check_injection(message):
        return JSONResponse(content={
            "code": 0,
            "data": {
                "reply": "抱歉，我无法处理这个请求。请提出正常的咨询问题，我来帮您解决。",
            },
            "msg": "success"
        })

    client_ip = req.client.host if req.client else "unknown"
    if not rate_limiter.check_session(session_id):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "咨询人数较多，请稍后再试"
        })
    if not rate_limiter.check_ip(client_ip):
        return JSONResponse(content={
            "code": -1,
            "data": None,
            "msg": "请求过于频繁，请稍后再试"
        })

    session_store.add_message(session_id, "user", message)
    
    context = session_store.get_conversation_history(session_id, max_rounds=3)

    async def stream_response():
        full_reply = ""
        stream_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        
        try:
            async for chunk in kimi_client.direct_response_stream(message, context):
                if chunk.strip():
                    lines = chunk.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            try:
                                line_data = line
                                if line.startswith('data: '):
                                    line_data = line[6:]
                                if line_data.strip() != '[DONE]':
                                    data = json.loads(line_data)
                                    if 'choices' in data and len(data['choices']) > 0:
                                        delta = data['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            content = delta['content']
                                            full_reply += content
                                            yield f"data: {json.dumps({'type': 'text', 'content': content, 'done': False})}\n\n"
                                    if 'usage' in data:
                                        stream_usage = {
                                            "prompt_tokens": data['usage'].get('prompt_tokens', 0),
                                            "completion_tokens": data['usage'].get('completion_tokens', 0),
                                            "total_tokens": data['usage'].get('total_tokens', 0),
                                        }
                            except Exception as parse_e:
                                print(f"[DEBUG] Parse error: {str(parse_e)} - line: {line[:100]}")
                                pass

            session_store.add_message(session_id, "assistant", full_reply)
            
            if stream_usage["total_tokens"] > 0:
                session_store.add_token_usage(session_id, stream_usage)
            
            accumulated_usage = session_store.get_session(session_id).get("token_usage", {})
            
            yield f"data: {json.dumps({
                'type': 'done',
                'content': full_reply,
                'done': True,
                'quick_actions': ['咨询商品', '查询订单', '处理售后'],
                'token_usage': accumulated_usage,
            })}\n\n"

        except Exception as e:
            import traceback
            error_log = f"Quick stream error: {str(e)}\n{traceback.format_exc()}"
            print(error_log)
            yield f"data: {json.dumps({'type': 'error', 'content': '抱歉，系统暂时遇到了一些问题', 'done': True})}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    session_store.delete_session(session_id)
    return JSONResponse(content={"code": 0, "data": None, "msg": "success"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
