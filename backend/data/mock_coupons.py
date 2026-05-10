MOCK_COUPONS = [
    {"coupon_id": "CPN-001", "name": "数码618专享券", "type": "满减券", "value": "减200元", "threshold": "满3000元", "category": "数码", "valid_period": "2026-05-01 ~ 2026-06-30", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-002", "name": "新人专享券", "type": "满减券", "value": "减50元", "threshold": "满199元", "category": "全品类", "valid_period": "领取后7天", "status": "有效", "target_users": "新注册用户"},
    {"coupon_id": "CPN-003", "name": "美妆满减券", "type": "满减券", "value": "减100元", "threshold": "满500元", "category": "美妆", "valid_period": "2026-05-01 ~ 2026-05-31", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-004", "name": "家居折扣券", "type": "折扣券", "value": "9折", "threshold": "满1000元", "category": "家居", "valid_period": "2026-05-01 ~ 2026-06-30", "status": "有效", "target_users": "金卡及以上会员"},
    {"coupon_id": "CPN-005", "name": "服装换季券", "type": "满减券", "value": "减80元", "threshold": "满399元", "category": "服装", "valid_period": "2026-05-01 ~ 2026-05-31", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-006", "name": "母婴关怀券", "type": "满减券", "value": "减150元", "threshold": "满599元", "category": "母婴", "valid_period": "2026-05-01 ~ 2026-12-31", "status": "有效", "target_users": "母婴品类购买用户"},
    {"coupon_id": "CPN-007", "name": "食品满减券", "type": "满减券", "value": "减30元", "threshold": "满199元", "category": "食品", "valid_period": "2026-05-01 ~ 2026-05-31", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-008", "name": "运动户外券", "type": "折扣券", "value": "8.5折", "threshold": "满300元", "category": "运动", "valid_period": "2026-05-01 ~ 2026-06-30", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-009", "name": "图书满减券", "type": "满减券", "value": "减20元", "threshold": "满100元", "category": "图书", "valid_period": "2026-05-01 ~ 2026-12-31", "status": "有效", "target_users": "全部用户"},
    {"coupon_id": "CPN-010", "name": "会员生日券", "type": "满减券", "value": "减100元", "threshold": "无门槛", "category": "全品类", "valid_period": "生日当月", "status": "有效", "target_users": "银卡及以上会员"},
]


def search_coupons(category=None, user_profile=None):
    """根据品类和用户画像检索可用优惠券"""
    results = MOCK_COUPONS
    if category:
        results = [c for c in results if c["category"] == category or c["category"] == "全品类"]
    if user_profile:
        membership = user_profile.get("membership_level", "")
        if membership in ["金卡会员", "钻石会员"]:
            pass
        else:
            results = [c for c in results if "金卡" not in c.get("target_users", "")]
    return results


def get_coupon_by_id(coupon_id):
    """根据ID获取优惠券"""
    for c in MOCK_COUPONS:
        if c["coupon_id"] == coupon_id:
            return c
    return None
