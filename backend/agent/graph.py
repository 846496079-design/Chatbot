import json
import uuid
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

from agent.state import AgentState
from api.kimi_client import kimi_client
from memory.session_store import session_store
from data.mock_products import search_products, get_product_by_id, recommend_by_scene
from data.mock_orders import search_orders, get_order_by_id
from data.mock_tickets import create_ticket
from utils.security import check_injection, mask_phone
from config import MAX_FALLBACK_ROUNDS, MAX_EMOTION_NEGATIVE_ROUNDS


# 英文值到中文的转换映射表
VALUE_TRANSLATION_MAP = {
    # 性别
    "female": "女", "male": "男",
    # 是否类
    "yes": "是", "no": "否", "true": "是", "false": "否",
    # 等级类
    "high": "高", "medium": "中", "low": "低",
    # 婚姻状况
    "married": "已婚", "single": "未婚", "divorced": "离异", "widowed": "丧偶",
    # 教育程度
    "bachelor": "本科", "master": "硕士", "doctor": "博士",
    "high school": "高中", "college": "大专", "phd": "博士",
    # 职业
    "engineer": "工程师", "teacher": "教师",
    "student": "学生", "designer": "设计师", "manager": "经理",
    "programmer": "程序员", "developer": "开发者",
    # 地域
    "beijing": "北京", "shanghai": "上海", "guangzhou": "广州",
    "shenzhen": "深圳", "hangzhou": "杭州", "chengdu": "成都",
    "nanjing": "南京", "wuhan": "武汉", "chongqing": "重庆",
    # 购物动机
    "self use": "自用", "gift": "送礼", "for family": "家用",
    "for work": "工作用", "personal": "自用",
    # 决策周期
    "short": "短", "long": "长",
    # 宠物
    "dog": "养狗", "cat": "养猫", "none": "无",
    # 兴趣爱好
    "reading": "阅读", "sports": "运动", "music": "音乐",
    "travel": "旅行", "gaming": "游戏", "photography": "摄影",
    "cooking": "烹饪", "fitness": "健身", "movie": "电影",
    # 生活标签
    "tech lover": "科技控", "fashion lover": "时尚达人",
    "foodie": "美食家", "traveler": "旅行者",
    # 品类
    "electronics": "数码", "clothing": "服装", "cosmetics": "美妆",
    "food": "食品", "home": "家居",
    "books": "图书", "toys": "玩具",
    # 品牌
    "apple": "Apple", "huawei": "华为", "xiaomi": "小米",
    "nike": "Nike", "adidas": "Adidas",
    # 支付方式
    "alipay": "支付宝", "wechat": "微信支付", "credit card": "信用卡",
    # 会员等级
    "regular": "普通会员", "silver": "银卡会员", "gold": "金卡会员",
    "platinum": "铂金会员", "diamond": "钻石会员",
    # 渠道
    "web": "网页", "app": "APP", "mini program": "小程序",
    # 活跃时段
    "morning": "上午", "afternoon": "下午", "evening": "晚间", "night": "深夜",
    # 联系方式
    "online": "在线客服", "phone": "电话", "email": "邮件",
    # 时尚风格
    "casual": "休闲", "formal": "正式", "sporty": "运动风",
    "business": "商务", "street": "街头",
    # 环保意识等
    "environmental": "环保", "not environmental": "不关注",
    # 品牌意识
    "brand conscious": "注重品牌", "not brand conscious": "不注重品牌",
    # 数码能力
    "tech savvy": "数码达人", "average": "一般", "beginner": "入门",
    # 新老客
    "new": "新客", "returning": "老客",
    # 设备类型
    "ios": "iOS", "android": "安卓", "pc": "电脑", "h5": "手机网页",
    # 促销敏感度
    "very sensitive": "非常敏感", "sensitive": "敏感", "not sensitive": "不敏感",
    # 浏览偏好
    "category browsing": "按品类浏览", "brand browsing": "按品牌浏览",
    "price sorting": "按价格排序", "sales sorting": "按销量排序",
    # 搜索行为
    "keyword search": "关键词搜索", "voice search": "语音搜索",
    "image search": "图片搜索", "filter search": "筛选搜索",
    # 评价行为
    "active reviewer": "活跃评价者", "occasional reviewer": "偶尔评价",
    "never review": "从不评价", "photo reviewer": "晒图评价者",
    # 客户生命周期
    "new customer": "新客户", "active customer": "活跃客户",
    "declining customer": "衰退客户", "lost customer": "流失客户",
    "loyal customer": "忠诚客户",
    # 通用
    "unknown": "未知", "other": "其他", "not sure": "不确定",
    "prefer not to say": "不愿透露",
    # 职业补充
    "self-employed": "自由职业", "unemployed": "无业", "retired": "退休",
    "housewife": "家庭主妇", "civil servant": "公务员",
    "medical": "医疗", "finance": "金融", "education": "教育",
    "it": "IT", "freelancer": "自由职业者", "business owner": "企业主",
    "white collar": "白领", "blue collar": "蓝领",
    # 地域补充
    "north": "北方", "south": "南方", "east": "东部", "west": "西部",
    "northeast": "东北", "southwest": "西南", "northwest": "西北", "southeast": "东南",
    "tier 1": "一线城市", "tier 2": "二线城市", "tier 3": "三线城市",
    "tier 4": "四线城市", "tier 5": "五线城市",
    "first-tier": "一线城市", "second-tier": "二线城市", "third-tier": "三线城市",
    "new tier 1": "新一线城市",
    # 购买频率
    "frequently": "频繁", "occasionally": "偶尔", "rarely": "很少",
    "daily": "每天", "weekly": "每周", "monthly": "每月",
    # 购物风格
    "impulsive": "冲动型", "planned": "计划型",
    "brand loyal": "品牌忠诚", "price driven": "价格驱动", "quality driven": "品质驱动",
    "early adopter": "早期尝鲜者", "mainstream": "主流用户", "late adopter": "晚期用户",
    "impulse buyer": "冲动购买者", "researcher": "研究型", "comparison shopper": "比价型",
    "loyal": "忠诚", "switcher": "摇摆型",
    "deal seeker": "优惠追求者", "convenience seeker": "便利追求者",
    "social shopper": "社交购物者", "solo shopper": "独立购物者",
    # 活跃时段补充
    "weekday": "工作日", "weekend": "周末",
    "morning person": "早起型", "night owl": "夜猫子",
    # 性格特征
    "patient": "耐心", "impatient": "急躁",
    "very patient": "非常耐心", "moderate": "适中",
    "introvert": "内向", "extrovert": "外向",
    # 宠物补充
    "cat person": "猫奴", "dog person": "狗奴", "both": "都喜欢", "neither": "都不喜欢",
    # 消费风格
    "minimalist": "极简主义", "maximalist": "极繁主义",
    "trendy": "潮流", "classic": "经典", "vintage": "复古",
    "budget": "预算型", "mid-range": "中端", "premium": "高端", "luxury": "奢侈",
    # 决策速度
    "fast": "快", "slow": "慢",
    # 渠道补充
    "mobile-first": "手机优先", "desktop-first": "电脑优先",
    "omnichannel": "全渠道", "online-only": "纯线上", "offline-only": "纯线下",
    # 影响来源
    "influenced by reviews": "受评价影响", "influenced by ads": "受广告影响",
    "influenced by friends": "受朋友影响",
}


def translate_profile_value(value):
    """将英文槽位值转换为中文"""
    if value is None:
        return None
    if isinstance(value, str):
        lower_val = value.strip().lower()
        if lower_val in VALUE_TRANSLATION_MAP:
            return VALUE_TRANSLATION_MAP[lower_val]
        return value
    if isinstance(value, list):
        return [translate_profile_value(v) for v in value]
    return value


def translate_profile_slots(profile_slots: dict) -> dict:
    """将画像槽位中的所有英文值转换为中文"""
    translated = {}
    for key, value in profile_slots.items():
        translated[key] = translate_profile_value(value)
    return translated


INTENT_ROUTE_MAP = {
    "pre_sale": "pre_sale_flow",
    "order_query": "order_query_flow",
    "after_sale": "after_sale_flow",
    "general": "general_flow",
    "chitchat": "chitchat_flow",
    "unknown": "fallback_flow",
}

PRE_SALE_SLOTS = ["product_category", "budget_range", "brand_preference", "usage_scenario", "special_requirement"]
ORDER_QUERY_SLOTS = ["order_id", "phone", "query_type"]
AFTER_SALE_SLOTS = ["order_id", "issue_type", "issue_description", "expectation"]


def get_required_slots(flow: str) -> list:
    """获取流程所需的槽位列表"""
    slot_map = {
        "pre_sale_flow": PRE_SALE_SLOTS,
        "order_query_flow": ORDER_QUERY_SLOTS,
        "after_sale_flow": AFTER_SALE_SLOTS,
    }
    return slot_map.get(flow, [])


def get_missing_slots(flow: str, filled_slots: dict) -> list:
    """获取缺失的槽位"""
    required = get_required_slots(flow)
    return [s for s in required if not filled_slots.get(s)]


async def intent_classifier_node(state: AgentState) -> AgentState:
    """意图识别节点：分析用户意图、情绪、槽位"""
    session_id = state["session_id"]
    messages = state["messages"]
    user_input = messages[-1].content if messages else ""

    if check_injection(user_input):
        return {
            **state,
            "current_intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
            "current_emotion": {"label": "neutral", "confidence": 1.0},
            "error": "检测到提示词注入",
        }

    context = session_store.get_conversation_history(session_id, max_rounds=5)
    if not context:
        context = "（新会话，无历史对话）"

    result = await kimi_client.classify_intent(user_input, context)

    if not result.get("success"):
        return {
            **state,
            "current_intent": {"id": "INT-UN-00", "name": "未知意图", "confidence": 0.0, "route": "fallback_flow"},
            "current_emotion": {"label": "neutral", "confidence": 0.5},
            "error": result.get("error", "意图识别失败"),
        }

    intent_id = result["intent"]
    route = INTENT_ROUTE_MAP.get(intent_id, "fallback_flow")
    intent_info = {
        "id": f"INT-{intent_id.upper()}",
        "name": intent_id,
        "confidence": result["confidence"],
        "route": route,
    }

    emotion_info = {
        "label": result["emotion"],
        "confidence": result["emotion_confidence"],
    }

    session_store.add_token_usage(session_id, result.get("usage", {}))

    current_flow = state.get("current_flow")
    new_flow = route

    if current_flow == "pre_sale_flow" and new_flow == "after_sale_flow":
        emotion_label = result.get("emotion", "neutral")
        if emotion_label in ("dissatisfied", "angry"):
            new_flow = "pre_sale_flow"

    if current_flow and current_flow != new_flow and current_flow != "fallback_flow":
        session_store.push_snapshot(session_id)

    business_slots = state.get("business_slots", {})
    new_business_slots = result.get("business_slots", {})
    for k, v in new_business_slots.items():
        if v and not business_slots.get(k):
            business_slots[k] = v

    profile_slots = result.get("profile_slots", {})
    
    # 将所有英文槽位值统一转换为中文
    profile_slots = translate_profile_slots(profile_slots)
    
    if "老公" in user_input:
        profile_slots["gender"] = "女"
    elif "老婆" in user_input:
        profile_slots["gender"] = "男"
    elif "男朋友" in user_input:
        profile_slots["gender"] = "女"
    elif "女朋友" in user_input:
        profile_slots["gender"] = "男"
    elif "妈妈" in user_input or "母亲" in user_input:
        profile_slots["gender"] = "女"
    elif "爸爸" in user_input or "父亲" in user_input:
        profile_slots["gender"] = "男"
    
    emotion_label = result.get("emotion", "neutral")
    emotion_score = {
        "neutral": 5,
        "dissatisfied": 3,
        "angry": 1
    }.get(emotion_label, 5)
    profile_slots["satisfaction_score"] = emotion_score * 10

    if profile_slots:
        session_store.update_user_profile(session_id, profile_slots)

    return {
        **state,
        "current_intent": intent_info,
        "current_emotion": emotion_info,
        "current_flow": new_flow,
        "business_slots": business_slots,
        "error": None,
    }


def emotion_analyzer_node(state: AgentState) -> AgentState:
    """情绪分析节点：判断是否需要安抚或转接"""
    emotion = state.get("current_emotion", {})
    emotion_label = emotion.get("label", "neutral")
    session_id = state["session_id"]

    negative_count = state.get("negative_emotion_count", 0)
    need_comfort = False
    need_escalation = False

    if emotion_label in ("dissatisfied", "angry"):
        negative_count += 1
        need_comfort = True
        if negative_count >= MAX_EMOTION_NEGATIVE_ROUNDS:
            need_escalation = True

    session_store.update_session(session_id, {
        "negative_emotion_count": negative_count,
        "need_comfort": need_comfort,
        "need_escalation": need_escalation,
    })

    return {
        **state,
        "negative_emotion_count": negative_count,
        "need_comfort": need_comfort,
        "need_escalation": need_escalation,
    }


def router_node(state: AgentState) -> AgentState:
    """路由节点：根据意图分发到对应处理器"""
    flow = state.get("current_flow", "fallback_flow")
    intent = state.get("current_intent", {})
    confidence = intent.get("confidence", 0)

    if confidence < 0.5:
        fallback_count = state.get("fallback_count", 0) + 1
        session_id = state["session_id"]
        session_store.update_session(session_id, {"fallback_count": fallback_count})
        return {**state, "current_flow": "fallback_flow", "fallback_count": fallback_count}

    return {**state, "current_flow": flow}


async def pre_sale_handler(state: AgentState) -> AgentState:
    """售前导购处理器"""
    session_id = state["session_id"]
    business_slots = state.get("business_slots", {})
    missing = get_missing_slots("pre_sale_flow", business_slots)

    if missing:
        state["current_step"] = "收集商品偏好"
        conversation_history = session_store.get_conversation_history(session_id)
        result = await kimi_client.generate_response(
            intent="售前导购",
            emotion=state.get("current_emotion", {}).get("label", "neutral"),
            flow_name="售前导购",
            filled_slots=business_slots,
            missing_slots=missing,
            business_data="暂无匹配数据",
            conversation_history=conversation_history,
        )

        if result.get("success"):
            session_store.add_token_usage(session_id, result.get("usage", {}))
            reply = result["reply"]
        else:
            reply = f"为了更好地为您推荐，能告诉我您想了解哪类商品吗？比如数码、服装、家居还是美妆呢？"

        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "收集商品偏好",
            "quick_actions": ["推荐手机", "推荐耳机", "有什么优惠", "看看服装"],
        }

    category = business_slots.get("product_category", "")
    brand = business_slots.get("brand_preference", "")
    budget = business_slots.get("budget_range", "")

    min_price = None
    max_price = None
    if budget:
        import re
        nums = re.findall(r"\d+", str(budget))
        if len(nums) >= 2:
            min_price, max_price = int(nums[0]), int(nums[1])
        elif len(nums) == 1:
            max_price = int(nums[0])

    products = search_products(category=category, brand=brand, min_price=min_price, max_price=max_price)
    if not products:
        products = search_products(keyword=category)[:5]

    products_data = products[:5]
    
    # 检查用户是否对之前的推荐感兴趣
    session = session_store.get_session(session_id)
    previously_recommended = session.get("recommended_products", [])
    user_interested = session.get("user_interested_in_product", False)
    
    # 如果用户没有表现出兴趣，不要重复推荐
    if previously_recommended and not user_interested:
        # 检查用户是否在追问商品
        user_input = ""
        messages = state.get("messages", [])
        if messages:
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.type == "human":
                    user_input = msg.content
                    break
        
        # 如果用户没有追问商品，只简单回应
        interest_keywords = ["怎么样", "多少钱", "详情", "看看", "推荐", "哪个", "对比", "区别", "好不好", "值得"]
        is_asking_about_product = any(kw in user_input for kw in interest_keywords)
        
        if not is_asking_about_product:
            reply = "亲还有其他需要帮忙的吗？比如查询订单或者处理售后问题~"
            session_store.add_message(session_id, "assistant", reply)
            return {
                **state,
                "messages": state["messages"] + [AIMessage(content=reply)],
                "current_step": "等待用户反馈",
                "quick_actions": ["查询订单", "处理售后", "咨询其他商品"],
            }
    
    # 记录本次推荐的商品
    session_store.update_session(session_id, {
        "recommended_products": [p["name"] for p in products_data]
    })
    
    # 检查用户是否要求下单
    user_input = ""
    messages = state.get("messages", [])
    if messages:
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "human":
                user_input = msg.content
                break
    
    order_keywords = ["下单", "买", "购买", "就要", "这个吧", "确定要", "好的，买", "行，买", "就它了", "现在就可以，怎么下单", "帮我下单", "我要下单"]
    is_ordering = any(kw in user_input for kw in order_keywords)
    
    if is_ordering and products_data:
        # 先回复确认消息
        product_name = products_data[0]["name"]
        price = products_data[0]["price"]
        pending_action = {
            "type": "order",
            "product": products_data[0]
        }
        session_store.update_session(session_id, {"pending_action": pending_action})
        reply = f"好的，我这就帮您操作😊 确认一下：您要购买{product_name}，金额{price}元，对吗？"
        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "下单确认",
            "quick_actions": ["确认下单", "再考虑一下"],
            "pending_action": pending_action
        }
    
    business_data = json.dumps(products_data, ensure_ascii=False, indent=2)
    conversation_history = session_store.get_conversation_history(session_id)
    result = await kimi_client.generate_response(
        intent="售前导购",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="售前导购",
        filled_slots=business_slots,
        missing_slots=[],
        business_data=business_data,
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        names = [p["name"] for p in products_data[:3]]
        reply = f"根据您的需求，为您推荐：{'、'.join(names)}。请问有感兴趣的吗？"

    session_store.add_message(session_id, "assistant", reply)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "商品推荐",
        "quick_actions": ["换一批推荐", "对比品牌", "查看详情", "咨询其他商品"],
        "cards": products_data,
        "card_type": "product",
    }


async def order_query_handler(state: AgentState) -> AgentState:
    """售中订单查询处理器"""
    session_id = state["session_id"]
    business_slots = state.get("business_slots", {})

    order_id = business_slots.get("order_id", "")
    phone = business_slots.get("phone", "")

    if not order_id and not phone:
        conversation_history = session_store.get_conversation_history(session_id)
        result = await kimi_client.generate_response(
            intent="订单查询",
            emotion=state.get("current_emotion", {}).get("label", "neutral"),
            flow_name="订单查询",
            filled_slots=business_slots,
            missing_slots=["order_id", "phone"],
            business_data="暂无数据",
            conversation_history=conversation_history,
        )

        if result.get("success"):
            session_store.add_token_usage(session_id, result.get("usage", {}))
            reply = result["reply"]
        else:
            reply = "请提供您的订单号，或者收货手机号后4位，我帮您查询哈。"

        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "收集订单信息",
            "quick_actions": ["ORD-20260502-002", "ORD-20260503-004", "ORD-20260504-005"],
        }

    order = None
    if order_id:
        order = get_order_by_id(order_id)
    if not order and phone:
        from data.mock_orders import get_orders_by_phone_suffix
        orders = get_orders_by_phone_suffix(phone)
        if orders:
            order = orders[0]

    if not order:
        reply = "抱歉，没有找到匹配的订单信息。请确认订单号是否正确，或者尝试用手机号后4位查询哦。"
        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "订单未找到",
            "quick_actions": ["重新输入订单号", "用手机号查询", "联系人工"],
        }

    business_data = json.dumps(order, ensure_ascii=False, indent=2)
    conversation_history = session_store.get_conversation_history(session_id)
    result = await kimi_client.generate_response(
        intent="订单查询",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="订单查询",
        filled_slots=business_slots,
        missing_slots=[],
        business_data=business_data,
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        logistics_info = ""
        if order.get("logistics"):
            logistics_info = f"，物流状态：{order['logistics']['current']}"
        reply = f"您的订单{order['order_id']}：{order['product_name']}，金额{order['amount']}元，状态：{order['status']}{logistics_info}。还需要其他帮助吗？"

    session_store.add_message(session_id, "assistant", reply)

    # 构建返回卡片数据
    return_cards = [order]
    card_type = "order"
    if order.get("logistics"):
        return_cards = [{**order["logistics"], "order_id": order["order_id"]}]
        card_type = "logistics"

    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "展示订单信息",
        "quick_actions": ["查看物流详情", "修改订单", "取消订单", "还有其他问题"],
        "cards": return_cards,
        "card_type": card_type,
    }


async def after_sale_handler(state: AgentState) -> AgentState:
    """售后客诉处理器"""
    session_id = state["session_id"]
    business_slots = state.get("business_slots", {})

    order_id = business_slots.get("order_id", "")
    issue_type = business_slots.get("issue_type", "")
    issue_desc = business_slots.get("issue_description", "")

    if not order_id:
        conversation_history = session_store.get_conversation_history(session_id)
        result = await kimi_client.generate_response(
            intent="售后处理",
            emotion=state.get("current_emotion", {}).get("label", "neutral"),
            flow_name="售后处理",
            filled_slots=business_slots,
            missing_slots=["order_id"],
            business_data="暂无数据",
            conversation_history=conversation_history,
        )

        if result.get("success"):
            session_store.add_token_usage(session_id, result.get("usage", {}))
            reply = result["reply"]
        else:
            reply = "请提供需要处理的订单号，我来帮您处理售后问题。"

        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "收集售后信息",
            "quick_actions": ["ORD-20260501-001", "ORD-20260504-006", "ORD-20260502-002"],
        }

    if not issue_type and not issue_desc:
        conversation_history = session_store.get_conversation_history(session_id)
        result = await kimi_client.generate_response(
            intent="售后处理",
            emotion=state.get("current_emotion", {}).get("label", "neutral"),
            flow_name="售后处理",
            filled_slots=business_slots,
            missing_slots=["issue_type", "issue_description"],
            business_data="暂无数据",
            conversation_history=conversation_history,
        )

        if result.get("success"):
            session_store.add_token_usage(session_id, result.get("usage", {}))
            reply = result["reply"]
        else:
            reply = "请问您遇到了什么问题呢？是想要退货、换货，还是商品有质量问题？"

        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "收集问题描述",
            "quick_actions": ["我要退货", "商品有质量问题", "申请换货", "查询退款进度"],
        }

    order = get_order_by_id(order_id)
    if not order:
        reply = f"抱歉，没有找到订单{order_id}的信息。请确认订单号是否正确哦。"
        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "订单未找到",
        }

    ticket = create_ticket(
        order_id=order_id,
        issue_type=issue_type or "未分类",
        description=issue_desc or "用户未提供详细描述",
        expectation=business_slots.get("expectation"),
    )
    
    # 检查用户是否要求退订/取消订单
    user_input = ""
    messages = state.get("messages", [])
    if messages:
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "human":
                user_input = msg.content
                break
    
    cancel_keywords = ["退订", "取消订单", "不要了", "退款", "退货", "取消", "我要退", "帮我退", "申请退款"]
    is_canceling = any(kw in user_input for kw in cancel_keywords) or (issue_type and "退" in issue_type)
    
    if is_canceling:
        # 先回复确认消息
        refund_amount = order["amount"]
        pending_action = {
            "type": "cancel",
            "order": order
        }
        session_store.update_session(session_id, {"pending_action": pending_action})
        reply = f"好的，我这就帮您操作😊 确认一下：您要取消订单{order_id}，商品{order['product_name']}，退款金额{refund_amount}元，对吗？"
        session_store.add_message(session_id, "assistant", reply)
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "退订确认",
            "quick_actions": ["确认取消", "再考虑一下"],
            "pending_action": pending_action
        }

    business_data = json.dumps({"order": order, "ticket": ticket}, ensure_ascii=False, indent=2)
    conversation_history = session_store.get_conversation_history(session_id)
    result = await kimi_client.generate_response(
        intent="售后处理",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="售后处理",
        filled_slots=business_slots,
        missing_slots=[],
        business_data=business_data,
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        reply = f"已为您创建售后工单（{ticket['ticket_id']}），处理{issue_type or '您的问题'}。预计{ticket['estimated_time']}内回复，请留意通知哦。"

    session_store.add_message(session_id, "assistant", reply)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "工单创建完成",
        "quick_actions": ["查看工单进度", "还有其他问题", "联系人工"],
    }


async def general_handler(state: AgentState) -> AgentState:
    """通用问题处理器"""
    session_id = state["session_id"]
    conversation_history = session_store.get_conversation_history(session_id)
    result = await kimi_client.generate_response(
        intent="通用咨询",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="通用咨询",
        filled_slots=state.get("business_slots", {}),
        missing_slots=[],
        business_data="通用客服场景，可回答账户、优惠券、会员、支付等问题",
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        reply = "亲，啥情况？跟我说说哈"

    session_store.add_message(session_id, "assistant", reply)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "通用回复",
        "quick_actions": ["查询订单", "浏览商品", "联系人工"],
    }


async def chitchat_handler(state: AgentState) -> AgentState:
    """闲聊处理器"""
    session_id = state["session_id"]
    conversation_history = session_store.get_conversation_history(session_id)

    # 获取用户最新输入，检查是否有场景关键词可以推荐商品
    user_input = ""
    messages = state.get("messages", [])
    if messages:
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "human":
                user_input = msg.content
                break

    # 检查用户是否对之前的推荐感兴趣
    session = session_store.get_session(session_id)
    previously_recommended = session.get("recommended_products", [])
    user_interested = session.get("user_interested_in_product", False)
    
    # 尝试场景化商品推荐
    scene_products = []
    if user_input:
        scene_products = recommend_by_scene(user_input, max_results=3)

    # 如果之前有推荐但用户没兴趣，且用户没有追问，就不重复推荐
    if previously_recommended and not user_interested and scene_products:
        interest_keywords = ["怎么样", "多少钱", "详情", "看看", "推荐", "哪个", "对比", "区别", "好不好", "值得", "怎么", "介绍"]
        is_asking_about_product = any(kw in user_input for kw in interest_keywords)
        
        if not is_asking_about_product:
            # 用户没有追问，只闲聊回应
            scene_products = []

    if scene_products:
        products_data = json.dumps(scene_products, ensure_ascii=False, indent=2)
        business_data = f"用户闲聊中透露出购买需求，推荐相关商品：\n{products_data}"
        # 记录本次推荐的商品
        session_store.update_session(session_id, {
            "recommended_products": [p["name"] for p in scene_products]
        })
    else:
        business_data = "用户在进行闲聊，需要友好回应并引导至服务场景"

    result = await kimi_client.generate_response(
        intent="闲聊",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="闲聊",
        filled_slots={},
        missing_slots=[],
        business_data=business_data,
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        if scene_products:
            names = [p["name"] for p in scene_products[:2]]
            reply = f"亲，顺便提一下，{'、'.join(names)}挺适合你的，有兴趣看看不？"
        else:
            reply = "您好呀！我是小慧，可以帮您推荐商品、查询订单、处理售后，有什么需要吗？"

    session_store.add_message(session_id, "assistant", reply)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "闲聊回复",
        "quick_actions": ["推荐商品", "查询订单", "处理售后"],
        "cards": scene_products if scene_products else None,
        "card_type": "product" if scene_products else None,
    }


async def fallback_handler(state: AgentState) -> AgentState:
    """异常兜底处理器"""
    session_id = state["session_id"]
    fallback_count = state.get("fallback_count", 0)

    if fallback_count >= MAX_FALLBACK_ROUNDS:
        reply = "非常抱歉，我暂时无法准确理解您的需求。建议您转接人工客服，他们会更快帮您解决问题。[转接人工]"
        session_store.add_message(session_id, "assistant", reply)
        session_store.update_session(session_id, {"need_escalation": True})
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "current_step": "转接人工",
            "need_escalation": True,
            "quick_actions": ["转接人工客服"],
        }

    conversation_history = session_store.get_conversation_history(session_id)
    result = await kimi_client.generate_response(
        intent="未知意图",
        emotion=state.get("current_emotion", {}).get("label", "neutral"),
        flow_name="兜底澄清",
        filled_slots={},
        missing_slots=[],
        business_data="无法识别用户意图，需要反问澄清",
        conversation_history=conversation_history,
    )

    if result.get("success"):
        session_store.add_token_usage(session_id, result.get("usage", {}))
        reply = result["reply"]
    else:
        reply = "亲，我没太懂~ 你是想：1.买东西 2.查订单 3.售后问题？"

    session_store.add_message(session_id, "assistant", reply)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=reply)],
        "current_step": "clarification",
        "quick_actions": ["咨询商品", "查询订单", "处理售后"],
    }


async def comfort_injector(state: AgentState) -> AgentState:
    """安抚注入节点：在需要时在回复前插入安抚话术"""
    if not state.get("need_comfort"):
        return state

    emotion_label = state.get("current_emotion", {}).get("label", "neutral")
    
    # 硬编码安抚话术，避免额外LLM调用
    comfort_texts = {
        "dissatisfied": "亲，我懂你",
        "angry": "亲别气，这事包我身上",
        "neutral": ""
    }
    
    comfort_text = comfort_texts.get(emotion_label, "")
    
    if comfort_text:
        messages = state["messages"]
        if messages and hasattr(messages[-1], "content"):
            last_msg = messages[-1]
            new_content = f"{comfort_text}。{last_msg.content}"
            new_messages = list(messages[:-1]) + [AIMessage(content=new_content)]
            return {**state, "messages": new_messages}

    return state


def route_by_flow(state: AgentState) -> Literal[
    "pre_sale_handler", "order_query_handler", "after_sale_handler",
    "general_handler", "chitchat_handler", "fallback_handler"
]:
    """根据流程路由到对应处理器"""
    flow = state.get("current_flow", "fallback_flow")
    route_map = {
        "pre_sale_flow": "pre_sale_handler",
        "order_query_flow": "order_query_handler",
        "after_sale_flow": "after_sale_handler",
        "general_flow": "general_handler",
        "chitchat_flow": "chitchat_handler",
        "fallback_flow": "fallback_handler",
    }
    return route_map.get(flow, "fallback_handler")


def build_graph() -> StateGraph:
    """构建LangGraph状态图"""
    workflow = StateGraph(AgentState)

    workflow.add_node("intent_classifier", intent_classifier_node)
    workflow.add_node("emotion_analyzer", emotion_analyzer_node)
    workflow.add_node("router", router_node)
    workflow.add_node("pre_sale_handler", pre_sale_handler)
    workflow.add_node("order_query_handler", order_query_handler)
    workflow.add_node("after_sale_handler", after_sale_handler)
    workflow.add_node("general_handler", general_handler)
    workflow.add_node("chitchat_handler", chitchat_handler)
    workflow.add_node("fallback_handler", fallback_handler)
    workflow.add_node("comfort_injector", comfort_injector)

    workflow.set_entry_point("intent_classifier")

    workflow.add_edge("intent_classifier", "emotion_analyzer")
    workflow.add_edge("emotion_analyzer", "router")

    workflow.add_conditional_edges(
        "router",
        route_by_flow,
        {
            "pre_sale_handler": "pre_sale_handler",
            "order_query_handler": "order_query_handler",
            "after_sale_handler": "after_sale_handler",
            "general_handler": "general_handler",
            "chitchat_handler": "chitchat_handler",
            "fallback_handler": "fallback_handler",
        }
    )

    workflow.add_edge("pre_sale_handler", "comfort_injector")
    workflow.add_edge("order_query_handler", "comfort_injector")
    workflow.add_edge("after_sale_handler", "comfort_injector")
    workflow.add_edge("general_handler", "comfort_injector")
    workflow.add_edge("chitchat_handler", "comfort_injector")
    workflow.add_edge("fallback_handler", "comfort_injector")

    workflow.add_edge("comfort_injector", END)

    return workflow.compile()


agent_graph = build_graph()
