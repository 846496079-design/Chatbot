import json
import httpx
from config import KIMI_API_KEY, KIMI_API_BASE, KIMI_MODEL, LLM_TIMEOUT, LLM_MAX_RETRIES


class KimiClient:
    def __init__(self):
        self.api_key = KIMI_API_KEY
        self.base_url = KIMI_API_BASE
        self.model = KIMI_MODEL
        self.timeout = LLM_TIMEOUT
        self.max_retries = LLM_MAX_RETRIES
        # 缓存常见意图的模式匹配，用于快速路由
        self.intent_patterns = {
            "order_query": ["订单", "物流", "单号", "发货", "快递", "tracking", "ORD-"],
            "after_sale": ["退货", "退款", "售后", "质量问题", "换货", "投诉"],
            "pre_sale": ["推荐", "买", "商品", "价格", "优惠", "折扣"],
            "chitchat": ["你好", "嗨", "在吗", "聊天", "天气", "时间"],
        }

    async def get_api_quota(self) -> dict:
        """查询API配额信息"""
        url = f"{self.base_url}/models"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # 从响应头获取配额信息
                    rate_limit = response.headers.get("x-ratelimit-limit", "未知")
                    rate_remaining = response.headers.get("x-ratelimit-remaining", "未知")
                    
                    return {
                        "success": True,
                        "message": "查询成功",
                        "rate_limit": rate_limit,
                        "rate_remaining": rate_remaining,
                        "model_info": data.get("data", [])[:3]  # 返回前3个模型信息
                    }
                else:
                    return {
                        "success": False,
                        "message": f"查询失败: {response.status_code}",
                        "detail": response.text
                    }
        except Exception as e:
            return {
                "success": False,
                "message": f"查询异常: {str(e)}"
            }

    async def chat(self, messages: list, temperature: float = 0.3) -> dict:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024
        }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "success": True,
                            "content": data["choices"][0]["message"]["content"],
                            "usage": {
                                "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                                "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
                                "total_tokens": data.get("usage", {}).get("total_tokens", 0)
                            }
                        }
                    elif response.status_code == 401:
                        last_error = "API Key无效或已过期，请检查配置"
                        break
                    elif response.status_code == 403:
                        last_error = "API Key权限不足，请检查API Key设置"
                        break
                    else:
                        last_error = f"API返回错误: {response.status_code} - {response.text}"
            except httpx.TimeoutException:
                last_error = "API调用超时，请检查网络连接"
            except httpx.ConnectError:
                last_error = "无法连接到API服务，请检查网络和API配置"
            except Exception as e:
                last_error = f"API调用异常: {str(e)}"

        return {"success": False, "error": last_error, "content": None, "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}

    async def chat_stream(self, messages: list, temperature: float = 0.3):
        """流式聊天方法"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024,
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code == 200:
                        async for chunk in response.aiter_text():
                            if chunk.strip():
                                yield chunk
                    else:
                        yield f"Error: {response.status_code}"
        except Exception as e:
            yield f"Error: {str(e)}"

    async def classify_intent(self, user_input: str, context: str) -> dict:
        from agent.prompts import INTENT_CLASSIFIER_PROMPT
        prompt = INTENT_CLASSIFIER_PROMPT.format(context=context, user_input=user_input)
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.1)
        return self._parse_intent_result(result)

    async def analyze(self, user_input: str, context: str) -> dict:
        """精简分析 - 使用短提示词快速完成意图+情绪+槽位抽取"""
        from agent.prompts import ANALYZE_PROMPT
        prompt = ANALYZE_PROMPT.format(context=context, user_input=user_input)
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.1)
        return self._parse_intent_result(result)

    async def generate_response(self, intent: str, emotion: str, flow_name: str,
                                 filled_slots: dict, missing_slots: list,
                                 business_data: str, conversation_history: str) -> dict:
        from agent.prompts import RESPONSE_GENERATOR_PROMPT
        prompt = RESPONSE_GENERATOR_PROMPT.format(
            intent=intent, emotion=emotion, flow_name=flow_name,
            filled_slots=filled_slots,
            missing_slots=missing_slots, business_data=business_data,
            conversation_history=conversation_history
        )
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.5)
        if result["success"]:
            content = result["content"]
            # 去除大模型可能添加的各种前缀
            for prefix in ["A:", "AI:", "Assistant:", "客服:", "小慧:", "回复:", "回:"]:
                if content.startswith(prefix):
                    content = content[len(prefix):].strip()
                    break
            reply = self._parse_structured_reply(content)
            return {"success": True, "reply": reply, "usage": result["usage"]}
        return result

    def _parse_structured_reply(self, content: str) -> str:
        """解析结构化回复【回】和【问】，合并为自然文本"""
        import re
        # 先去除大模型可能添加的各种前缀
        for prefix in ["A:", "AI:", "Assistant:", "客服:", "小慧:", "回复:", "回:"]:
            if content.startswith(prefix):
                content = content[len(prefix):].strip()
                break

        hui_match = re.search(r'【回】\s*(.+?)(?:【问】|$)', content, re.DOTALL)
        wen_match = re.search(r'【问】\s*(.+?)$', content, re.DOTALL)

        hui_text = hui_match.group(1).strip() if hui_match else ""
        wen_text = wen_match.group(1).strip() if wen_match else ""

        if not hui_text:
            return content.strip()

        if wen_text:
            return f"{hui_text}\n{wen_text}"
        return hui_text

    async def generate_comfort(self, emotion: str) -> dict:
        from agent.prompts import EMOTION_COMFORT_PROMPT
        prompt = EMOTION_COMFORT_PROMPT.format(emotion=emotion)
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.5)
        if result["success"]:
            return {"success": True, "comfort_text": result["content"], "usage": result["usage"]}
        return result

    async def extract_profile(self, conversation: str, existing_profile: dict) -> dict:
        from agent.prompts import PROFILE_EXTRACTION_PROMPT
        from agent.graph import translate_profile_slots
        prompt = PROFILE_EXTRACTION_PROMPT.format(
            conversation=conversation, existing_profile=json.dumps(existing_profile, ensure_ascii=False)
        )
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.2)
        if result["success"]:
            try:
                content = result["content"].strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                parsed = json.loads(content)
                updates = translate_profile_slots(parsed.get("updates", {}))
                confidence = parsed.get("confidence", {})
                return {"success": True, "updates": updates, "confidence": confidence, "usage": result["usage"]}
            except json.JSONDecodeError:
                return {"success": True, "updates": {}, "usage": result["usage"]}
        return result

    def quick_intent_detect(self, user_input: str) -> str:
        """快速意图检测 - 使用模式匹配避免LLM调用"""
        user_input_lower = user_input.lower()
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.lower() in user_input_lower:
                    return intent
        return "general"

    async def direct_response(self, user_input: str, context: str = "") -> dict:
        """直接响应模式 - 跳过意图识别，直接生成响应（大幅降低首字延迟）"""
        from agent.prompts import DIRECT_RESPONSE_PROMPT
        prompt = DIRECT_RESPONSE_PROMPT.format(context=context, user_input=user_input)
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.5)
        if result["success"]:
            content = result["content"]
            # 去除大模型可能添加的各种前缀
            for prefix in ["A:", "AI:", "Assistant:", "客服:", "小慧:", "回复:", "回:"]:
                if content.startswith(prefix):
                    content = content[len(prefix):].strip()
                    break
            return {"success": True, "reply": content.strip(), "usage": result["usage"]}
        return result

    async def direct_response_stream(self, user_input: str, context: str = ""):
        """直接响应模式（流式）- 跳过意图识别，直接流式生成响应"""
        from agent.prompts import DIRECT_RESPONSE_PROMPT
        prompt = DIRECT_RESPONSE_PROMPT.format(context=context, user_input=user_input)
        messages = [{"role": "user", "content": prompt}]
        async for chunk in self.chat_stream(messages, temperature=0.5):
            yield chunk

    def _parse_intent_result(self, result: dict) -> dict:
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "未知错误"),
                "intent": "unknown",
                "confidence": 0.0,
                "emotion": "neutral",
                "emotion_confidence": 0.5,
                "profile_slots": {},
                "profile_confidence": {},
                "business_slots": {},
                "business_confidence": {},
                "usage": result.get("usage", {})
            }

        try:
            content = result["content"].strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            parsed = json.loads(content)
            return {
                "success": True,
                "intent": parsed.get("intent", "unknown"),
                "confidence": parsed.get("confidence", 0.0),
                "emotion": parsed.get("emotion", "neutral"),
                "emotion_confidence": parsed.get("emotion_confidence", 0.5),
                "profile_slots": parsed.get("profile_slots", {}),
                "profile_confidence": parsed.get("profile_confidence", {}),
                "business_slots": parsed.get("business_slots", {}),
                "business_confidence": parsed.get("business_confidence", {}),
                "reasoning": parsed.get("reasoning", ""),
                "usage": result.get("usage", {})
            }
        except (json.JSONDecodeError, KeyError) as e:
            return {
                "success": False,
                "error": f"解析失败: {str(e)}",
                "intent": "unknown",
                "confidence": 0.0,
                "emotion": "neutral",
                "emotion_confidence": 0.5,
                "profile_slots": {},
                "profile_confidence": {},
                "business_slots": {},
                "business_confidence": {},
                "usage": result.get("usage", {})
            }


kimi_client = KimiClient()