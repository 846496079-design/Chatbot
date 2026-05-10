MOCK_CONVERSATIONS = {
    "USER-001": [
        {
            "session_id": "SESS-001",
            "rounds": [
                {"round": 1, "role": "user", "content": "推荐一款高端手机", "profile_extracted": {"preferred_categories": ["数码"]}},
                {"round": 1, "role": "assistant", "content": "好的！您预算大概多少呢？", "profile_extracted": {}},
                {"round": 2, "role": "user", "content": "1万以内都行，主要看品质", "profile_extracted": {"consumption_level": "高", "budget_range": "10000"}},
                {"round": 2, "role": "assistant", "content": "推荐iPhone 16 Pro Max，9999元，A18芯片，专业级摄像系统。您觉得怎么样？", "profile_extracted": {}},
                {"round": 3, "role": "user", "content": "就它了，下单", "profile_extracted": {"decision_cycle": "短"}},
                {"round": 3, "role": "assistant", "content": "好的！已为您生成订单，祝您购物愉快！", "profile_extracted": {}},
            ]
        },
        {
            "session_id": "SESS-002",
            "rounds": [
                {"round": 1, "role": "user", "content": "ORD-20260501-001物流到哪了", "profile_extracted": {"order_id": "ORD-20260501-001"}},
                {"round": 1, "role": "assistant", "content": "您的iPhone已到达北京顺义集散中心，预计明天派送。", "profile_extracted": {"region": "北京"}},
                {"round": 2, "role": "user", "content": "好的，另外推荐一款扫地机器人", "profile_extracted": {"preferred_categories": ["家居"]}},
                {"round": 2, "role": "assistant", "content": "推荐科沃斯X2智能扫地机器人，3299元，全能扫拖，AI避障。以旧换新还能减300。", "profile_extracted": {}},
                {"round": 3, "role": "user", "content": "买了", "profile_extracted": {"repurchase_intent": "高"}},
                {"round": 3, "role": "assistant", "content": "好的！已为您下单科沃斯X2，预计2-3天送达。", "profile_extracted": {}},
            ]
        }
    ],
    "USER-002": [
        {
            "session_id": "SESS-003",
            "rounds": [
                {"round": 1, "role": "user", "content": "有没有便宜点的连衣裙", "profile_extracted": {"preferred_categories": ["服装"], "price_sensitivity": "高"}},
                {"round": 1, "role": "assistant", "content": "推荐伊芙丽女士碎花连衣裙，399元，法式复古风，透气亲肤。目前2件8折哦。", "profile_extracted": {}},
                {"round": 2, "role": "user", "content": "有优惠券吗？能再便宜点吗", "profile_extracted": {"price_sensitivity": "高"}},
                {"round": 2, "role": "assistant", "content": "目前有服装换季券，满399减80，折后319元。很划算呢！", "profile_extracted": {}},
                {"round": 3, "role": "user", "content": "那还行，我再看看别的", "profile_extracted": {"decision_cycle": "长"}},
                {"round": 3, "role": "assistant", "content": "好的，有需要随时找我哦！", "profile_extracted": {}},
            ]
        }
    ],
    "USER-003": []
}


def get_user_conversations(user_id):
    """获取用户历史会话记录"""
    return MOCK_CONVERSATIONS.get(user_id, [])


def get_user_stats(user_id):
    """获取用户会话统计数据"""
    conversations = get_user_conversations(user_id)
    total_rounds = sum(len(sess["rounds"]) for sess in conversations)
    return {
        "total_sessions": len(conversations),
        "total_rounds": total_rounds,
        "last_active": conversations[-1]["rounds"][-1]["round"] if conversations else None
    }
