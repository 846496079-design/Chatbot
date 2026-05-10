import traceback
import asyncio
from agent.graph import agent_graph
from langchain_core.messages import HumanMessage


async def test_graph():
    print("=== 测试Agent Graph ===")
    
    try:
        initial_state = {
            "messages": [HumanMessage(content="我要退货")],
            "session_id": "test_session_123",
            "current_intent": None,
            "current_emotion": None,
            "current_flow": None,
            "current_step": None,
            "business_slots": {},
            "user_profile": {},
            "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "fallback_count": 0,
            "negative_emotion_count": 0,
            "snapshot_stack": [],
            "need_escalation": False,
            "need_comfort": False,
            "quick_actions": [],
            "error": None,
        }
        
        print("调用agent_graph.ainvoke...")
        result = await agent_graph.ainvoke(initial_state)
        print("调用成功！")
        print(f"结果类型: {type(result)}")
        print(f"current_intent: {result.get('current_intent')}")
        print(f"current_emotion: {result.get('current_emotion')}")
        print(f"current_flow: {result.get('current_flow')}")
        print(f"messages: {result.get('messages')}")
        
    except Exception as e:
        print(f"调用失败: {str(e)}")
        print("完整堆栈:")
        print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(test_graph())