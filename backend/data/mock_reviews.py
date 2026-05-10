MOCK_REVIEWS = [
    {"review_id": "REV-001", "product_id": "PROD-001", "user": "张先生", "rating": 5, "content": "iPhone一如既往的流畅，A18芯片性能确实强，拍照效果惊艳。就是价格有点贵，但物有所值。", "tags": ["性能强劲", "拍照好", "价格偏高"], "time": "2026-05-03"},
    {"review_id": "REV-002", "product_id": "PROD-001", "user": "李女士", "rating": 4, "content": "手机很好用，但是发货有点慢，等了3天才发货。手机本身没得说。", "tags": ["物流慢", "品质好"], "time": "2026-05-05"},
    {"review_id": "REV-003", "product_id": "PROD-002", "user": "王先生", "rating": 5, "content": "华为Mate 70 Pro太香了！卫星通信功能在户外很有用，拍照XMAGE调教得很好。限时降1000性价比很高。", "tags": ["性价比高", "拍照好", "黑科技"], "time": "2026-05-04"},
    {"review_id": "REV-004", "product_id": "PROD-002", "user": "赵女士", "rating": 3, "content": "手机不错但发热有点严重，玩游戏的时候明显感觉烫手。希望后续系统更新能优化。", "tags": ["发热", "系统待优化"], "time": "2026-05-06"},
    {"review_id": "REV-005", "product_id": "PROD-008", "user": "刘先生", "rating": 5, "content": "Nike Air Max穿着很舒服，气垫缓震效果好，跑步不累脚。颜值也在线，日常穿搭也很百搭。", "tags": ["舒适", "百搭", "颜值高"], "time": "2026-05-02"},
    {"review_id": "REV-006", "product_id": "PROD-011", "user": "周先生", "rating": 5, "content": "科沃斯X2真的解放双手！扫拖一体很干净，AI避障很智能，家里有猫也不怕撞到。以旧换新还减了300。", "tags": ["智能", "干净", "宠物友好"], "time": "2026-05-05"},
    {"review_id": "REV-007", "product_id": "PROD-011", "user": "吴女士", "rating": 4, "content": "扫地效果不错，就是噪音稍微有点大，不适合晚上用。APP操作还算方便。", "tags": ["噪音偏大", "效果好"], "time": "2026-05-07"},
    {"review_id": "REV-008", "product_id": "PROD-016", "user": "陈女士", "rating": 5, "content": "兰蔻小黑瓶真的绝了！用了7天皮肤明显变细腻，吸收很快不油腻。赠品小样也很实用。", "tags": ["效果好", "吸收快", "赠品好"], "time": "2026-05-03"},
    {"review_id": "REV-009", "product_id": "PROD-019", "user": "郑女士", "rating": 4, "content": "雅诗兰黛DW粉底液确实是油皮亲妈，持妆一整天不脱妆。就是色号选择太多了，建议先去专柜试色。", "tags": ["持妆久", "控油", "色号多"], "time": "2026-05-04"},
    {"review_id": "REV-010", "product_id": "PROD-036", "user": "孙先生", "rating": 5, "content": "三体不愧是神作！刘慈欣的想象力太震撼了，黑暗森林法则让人深思。印刷质量也很好。", "tags": ["经典", "想象力", "印刷好"], "time": "2026-05-01"},
]


def get_reviews_by_product(product_id):
    """获取指定商品的评价列表"""
    return [r for r in MOCK_REVIEWS if r["product_id"] == product_id]


def get_review_summary(product_id):
    """获取商品评价摘要统计"""
    reviews = get_reviews_by_product(product_id)
    if not reviews:
        return {"count": 0, "avg_rating": 0, "positive_rate": 0}
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    positive_count = sum(1 for r in reviews if r["rating"] >= 4)
    return {
        "count": len(reviews),
        "avg_rating": round(avg_rating, 1),
        "positive_rate": round(positive_count / len(reviews) * 100, 1)
    }
