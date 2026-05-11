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

    async def chat(self, messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> dict:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
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

    def local_extract(self, user_input: str) -> dict:
        """本地预抽取：正则+关键词提取确定性槽位，减少LLM工作量，降低延迟"""
        import re
        result = {
            "business_slots": {},
            "business_confidence": {},
            "profile_slots": {},
            "profile_confidence": {},
            "intent": None,
            "intent_confidence": 0,
            "emotion": "neutral",
            "emotion_confidence": 0,
            "hints": ""
        }

        # === 订单号 ===
        order_match = re.search(r'ORD-\d{8}-\d{3}', user_input, re.IGNORECASE)
        if order_match:
            result["business_slots"]["order_id"] = order_match.group(0)
            result["business_confidence"]["order_id"] = 0.95
            result["hints"] += "已预提取订单号。"

        # === 手机号 ===
        phone_match = re.search(r'1[3-9]\d{9}', user_input)
        if phone_match:
            result["business_slots"]["phone"] = phone_match.group(0)
            result["business_confidence"]["phone"] = 0.9
            result["hints"] += "已预提取手机号。"

        tail_match = re.search(r'尾号\s*(\d{4})', user_input)
        if tail_match and "phone" not in result["business_slots"]:
            result["business_slots"]["phone"] = tail_match.group(1)
            result["business_confidence"]["phone"] = 0.85
            result["hints"] += "已预提取手机尾号。"

        # === 商品类别 ===
        category_map = {
            "手机": ["手机", "iphone", "华为手机", "小米手机", "oppo", "vivo", "三星手机"],
            "电脑": ["电脑", "笔记本", "台式机", "macbook", "thinkpad", "平板", "ipad"],
            "耳机": ["耳机", "耳塞", "airpods", "降噪耳机", "蓝牙耳机", "头戴式"],
            "服装": ["衣服", "服装", "外套", "裤子", "裙子", "T恤", "衬衫", "卫衣", "羽绒服"],
            "鞋类": ["鞋", "运动鞋", "跑鞋", "篮球鞋", "板鞋", "靴子", "凉鞋", "拖鞋"],
            "美妆": ["化妆品", "护肤品", "口红", "粉底", "面膜", "精华", "防晒", "洗面奶"],
            "家居": ["家具", "家居", "床", "沙发", "桌子", "椅子", "灯具", "窗帘", "枕头", "乳胶枕"],
            "家电": ["冰箱", "洗衣机", "空调", "电视", "扫地机", "吸尘器", "微波炉", "烤箱"],
            "图书": ["书", "图书", "小说", "教材", "绘本"],
            "食品": ["零食", "食品", "饮料", "茶叶", "咖啡", "坚果"],
            "母婴": ["宝宝", "婴儿", "奶粉", "尿布", "童装", "玩具", "推车"],
            "运动": ["跑步", "健身", "瑜伽", "游泳", "篮球", "足球", "羽毛球", "跳绳"],
            "箱包": ["包", "背包", "行李箱", "钱包", "双肩包"],
            "手表": ["手表", "手环", "智能手表", "apple watch"],
            "数码配件": ["充电器", "数据线", "充电宝", "手机壳", "支架", "U盘"],
        }
        for category, keywords in category_map.items():
            for kw in keywords:
                if kw.lower() in user_input.lower():
                    result["business_slots"]["product_category"] = category
                    result["business_confidence"]["product_category"] = 0.85
                    result["hints"] += f"已预提取商品类别:{category}。"
                    break
            if "product_category" in result["business_slots"]:
                break

        # === 品牌 ===
        brand_map = {
            "华为": ["华为", "huawei", "mate", "pura"],
            "苹果": ["苹果", "apple", "iphone", "ipad", "macbook", "airpods"],
            "小米": ["小米", "xiaomi", "红米", "redmi"],
            "OPPO": ["oppo"],
            "vivo": ["vivo"],
            "三星": ["三星", "samsung"],
            "Nike": ["nike", "耐克"],
            "Adidas": ["adidas", "阿迪达斯"],
            "安踏": ["安踏", "anta"],
            "李宁": ["李宁", "lining"],
            "兰蔻": ["兰蔻", "lancome"],
            "雅诗兰黛": ["雅诗兰黛", "estee lauder"],
            "戴森": ["戴森", "dyson"],
            "索尼": ["索尼", "sony"],
            "Bose": ["bose"],
            "美的": ["美的", "midea"],
            "格力": ["格力", "gree"],
            "海尔": ["海尔", "haier"],
        }
        for brand, keywords in brand_map.items():
            for kw in keywords:
                if kw.lower() in user_input.lower():
                    result["business_slots"]["brand_preference"] = brand
                    result["business_confidence"]["brand_preference"] = 0.85
                    result["hints"] += f"已预提取品牌:{brand}。"
                    break
            if "brand_preference" in result["business_slots"]:
                break

        # === 预算范围 ===
        budget_patterns = [
            (r'预算\s*(\d+)\s*[-~到至]\s*(\d+)', lambda m: f"{m.group(1)}-{m.group(2)}"),
            (r'(\d+)\s*[-~到至]\s*(\d+)\s*[块元]', lambda m: f"{m.group(1)}-{m.group(2)}"),
            (r'(\d+)\s*[块元]?[以之]?[内下]', lambda m: f"0-{m.group(1)}"),
            (r'(\d+)\s*[块元]?[以之]?[上外]', lambda m: f"{m.group(1)}+"),
            (r'预算\s*(\d+)', lambda m: f"约{m.group(1)}"),
            (r'(\d{3,5})\s*[块元]', lambda m: f"约{m.group(1)}"),
        ]
        for pattern, formatter in budget_patterns:
            m = re.search(pattern, user_input)
            if m:
                result["business_slots"]["budget_range"] = formatter(m)
                result["business_confidence"]["budget_range"] = 0.8
                result["hints"] += f"已预提取预算:{formatter(m)}。"
                break

        # === 使用场景 ===
        scene_map = {
            "送礼": ["送礼", "礼物", "送朋友", "送父母", "送老婆", "送老公", "送女朋友", "送男朋友", "生日礼物", "节日礼物"],
            "办公": ["办公", "工作", "上班", "商务", "开会"],
            "游戏": ["游戏", "打游戏", "吃鸡", "王者", "lol", "原神", "电竞"],
            "学习": ["学习", "上课", "考研", "考试", "网课", "学生"],
            "旅行": ["旅行", "旅游", "出差", "出行"],
            "运动": ["运动", "跑步", "健身", "锻炼"],
            "自用": ["自用", "自己用", "个人用"],
            "家用": ["家用", "家里用", "家庭"],
        }
        for scene, keywords in scene_map.items():
            for kw in keywords:
                if kw in user_input:
                    result["business_slots"]["usage_scenario"] = scene
                    result["business_confidence"]["usage_scenario"] = 0.8
                    result["hints"] += f"已预提取场景:{scene}。"
                    break
            if "usage_scenario" in result["business_slots"]:
                break

        # === 售后问题类型 ===
        issue_map = {
            "退货": ["退货", "退掉", "不要了", "退回去"],
            "退款": ["退款", "退钱", "还钱"],
            "换货": ["换货", "换一个", "换个"],
            "质量问题": ["坏了", "质量问题", "有瑕疵", "破损", "坏了", "不能用", "故障", "屏幕", "划痕"],
            "物流问题": ["物流", "快递", "没收到", "送错", "延误"],
            "投诉": ["投诉", "举报", "差评"],
        }
        for issue, keywords in issue_map.items():
            for kw in keywords:
                if kw in user_input:
                    result["business_slots"]["issue_type"] = issue
                    result["business_confidence"]["issue_type"] = 0.85
                    result["hints"] += f"已预提取问题类型:{issue}。"
                    break
            if "issue_type" in result["business_slots"]:
                break

        # === 意图检测 ===
        if "order_id" in result["business_slots"] or any(kw in user_input for kw in ["订单", "物流", "快递", "发货", "单号"]):
            result["intent"] = "order_query"
            result["intent_confidence"] = 0.9
        elif "issue_type" in result["business_slots"] or any(kw in user_input for kw in ["退货", "退款", "售后", "换货", "投诉", "坏了"]):
            result["intent"] = "after_sale"
            result["intent_confidence"] = 0.9
        elif "product_category" in result["business_slots"] or any(kw in user_input for kw in ["推荐", "买", "想买", "有没有", "多少钱", "价格", "优惠"]):
            result["intent"] = "pre_sale"
            result["intent_confidence"] = 0.85
        elif any(kw in user_input for kw in ["你好", "嗨", "在吗", "谢谢", "再见", "拜拜"]):
            result["intent"] = "chitchat"
            result["intent_confidence"] = 0.9

        # === 情绪检测 ===
        angry_words = ["垃圾", "烂", "坑", "骗", "投诉", "举报", "差劲", "太差", "气死", "火大", "混蛋", "傻逼", "sb", "尼玛", "卧槽"]
        dissatisfied_words = ["慢", "等了好久", "怎么回事", "不满意", "不行", "不好", "失望", "烦", "郁闷", "坑爹", "无语", "醉了"]
        for w in angry_words:
            if w in user_input:
                result["emotion"] = "angry"
                result["emotion_confidence"] = 0.9
                break
        if result["emotion"] == "neutral":
            for w in dissatisfied_words:
                if w in user_input:
                    result["emotion"] = "dissatisfied"
                    result["emotion_confidence"] = 0.85
                    break

        # === 画像槽位 ===
        if "老公" in user_input or "男朋友" in user_input:
            result["profile_slots"]["gender"] = "女"
            result["profile_confidence"]["gender"] = 0.9
        elif "老婆" in user_input or "女朋友" in user_input:
            result["profile_slots"]["gender"] = "男"
            result["profile_confidence"]["gender"] = 0.9
        elif "妈妈" in user_input or "母亲" in user_input:
            result["profile_slots"]["gender"] = "女"
            result["profile_confidence"]["gender"] = 0.85
        elif "爸爸" in user_input or "父亲" in user_input:
            result["profile_slots"]["gender"] = "男"
            result["profile_confidence"]["gender"] = 0.85

        if "宝宝" in user_input or "孩子" in user_input or "小孩" in user_input:
            result["profile_slots"]["has_children"] = "是"
            result["profile_confidence"]["has_children"] = 0.85

        if "学生" in user_input:
            result["profile_slots"]["age_range"] = "18-24岁"
            result["profile_confidence"]["age_range"] = 0.7

        if not result["hints"]:
            result["hints"] = "无"

        return result

    async def classify_intent(self, user_input: str, context: str) -> dict:
        from agent.prompts import INTENT_CLASSIFIER_PROMPT
        prompt = INTENT_CLASSIFIER_PROMPT.format(context=context, user_input=user_input)
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.1)
        return self._parse_intent_result(result)

    async def analyze(self, user_input: str, context: str) -> dict:
        """精简分析 - 本地意图/情绪 + LLM槽位/画像，大幅降低延迟"""
        from agent.prompts import ANALYZE_PROMPT

        pre = self.local_extract(user_input)

        prompt = ANALYZE_PROMPT.format(
            pre_extracted=pre["hints"],
            context=context,
            user_input=user_input
        )
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat(messages, temperature=0.1, max_tokens=200)

        parsed = self._parse_intent_result(result)

        if parsed.get("success"):
            for key, value in pre["business_slots"].items():
                if value:
                    parsed["business_slots"][key] = value
                    parsed["business_confidence"][key] = pre["business_confidence"].get(key, 0.9)

            for key, value in pre["profile_slots"].items():
                if value:
                    existing = parsed.get("profile_slots", {}).get(key)
                    if not existing:
                        parsed["profile_slots"][key] = value
                        parsed["profile_confidence"][key] = pre["profile_confidence"].get(key, 0.85)

        if pre["intent"] and pre["intent_confidence"] >= 0.8:
            parsed["intent"] = pre["intent"]
            parsed["confidence"] = pre["intent_confidence"]

        if pre["emotion_confidence"] >= 0.8:
            parsed["emotion"] = pre["emotion"]
            parsed["emotion_confidence"] = pre["emotion_confidence"]

        return parsed

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