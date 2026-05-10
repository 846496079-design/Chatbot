# -*- coding: utf-8 -*-
"""
用户画像40槽位测试用例（自然对话版）

设计原则：
1. 不自我介绍，信息通过购物语境自然泄露
2. 模拟真实电商对话：问商品、问价格、问物流、投诉、闲聊
3. 槽位按价值排序：高频高价值在前，低频低价值在后
"""

TEST_CASES = [
    # ============================================================
    # 场景1：给老婆挑生日礼物
    # 自然泄露：gender(男), marital_status(已婚), shopping_motivation(送礼),
    #           preferred_categories(美妆), brand_affinity(雅诗兰黛),
    #           price_sensitivity(中), consumption_level(中高),
    #           decision_cycle(短), income_level(中高), region(上海),
    #           living_city_tier(一线城市), new_vs_returning(老客)
    # ============================================================
    {
        "name": "给老婆挑生日礼物",
        "intent": "pre_sale",
        "description": "男性用户想给老婆买护肤品作为生日礼物",
        "conversation": [
            {"role": "user", "content": "老婆快过生日了，想给她买套护肤品，有什么推荐吗？"},
            {"role": "assistant", "content": "送老婆护肤品是很贴心的选择呢！请问您老婆平时用什么品牌？大概什么价位比较合适？"},
            {"role": "user", "content": "她一直用雅诗兰黛的，预算一千左右吧，别太便宜拿不出手。最好这两天就能到，生日快到了。"},
            {"role": "assistant", "content": "雅诗兰黛的礼盒套装很适合送礼，红石榴系列口碑很好，980元一套，包装也很精美。"},
            {"role": "user", "content": "行就这个吧，帮我下单，发上海浦东。对了你们能包装成礼物吗？之前买过几次了，包装都挺好的。"},
        ],
        "expected_slots": {
            "gender": "男",
            "marital_status": "已婚",
            "shopping_motivation": "送礼",
            "preferred_categories": ["美妆"],
            "brand_affinity": ["雅诗兰黛"],
            "price_sensitivity": "中",
            "consumption_level": "中高",
            "decision_cycle": "短",
            "income_level": "中高",
            "region": "上海",
            "living_city_tier": "一线城市",
            "new_vs_returning": "老客",
        },
    },

    # ============================================================
    # 场景2：学生党求推荐便宜耳机
    # 自然泄露：age_range(20-25), gender(男), income_level(低),
    #           price_sensitivity(高), preferred_categories(数码),
    #           consumption_level(低), preferred_payment_method(支付宝),
    #           coupon_usage_rate(高), hobbies(游戏/音乐),
    #           tech_savviness(数码达人), promotion_sensitivity(非常敏感),
    #           new_vs_returning(新客), browse_preference(按价格排序)
    # ============================================================
    {
        "name": "学生党求推荐便宜耳机",
        "intent": "pre_sale",
        "description": "大学生想买个便宜蓝牙耳机打游戏用",
        "conversation": [
            {"role": "user", "content": "有没有两百以内的蓝牙耳机？打游戏延迟低的那种"},
            {"role": "assistant", "content": "有的，QCY和漫步者都有入门款，延迟在60ms以内，适合游戏。您平时主要玩什么游戏呢？"},
            {"role": "user", "content": "吃鸡和王者，宿舍开黑用。学生党没啥钱，性价比高就行。对了能分期吗？花呗额度不太够。"},
            {"role": "assistant", "content": "支持花呗分期，3期免息。QCY T13券后169元，学生认证还能再减10块。"},
            {"role": "user", "content": "有券就好，我买东西都先看有没有券，按价格从低到高排着看。就这个吧，支付宝付。"},
        ],
        "expected_slots": {
            "age_range": "20-25",
            "gender": "男",
            "income_level": "低",
            "price_sensitivity": "高",
            "preferred_categories": ["数码"],
            "consumption_level": "低",
            "preferred_payment_method": "支付宝",
            "coupon_usage_rate": "高",
            "hobbies": ["游戏", "音乐"],
            "tech_savviness": "数码达人",
            "promotion_sensitivity": "非常敏感",
            "new_vs_returning": "新客",
            "browse_preference": "按价格排序",
        },
    },

    # ============================================================
    # 场景3：收到坏的商品要退货
    # 自然泄露：complaint_tendency(高), satisfaction_score(低),
    #           response_patience(低), return_rate(高),
    #           channel_preference(APP), active_time(晚间),
    #           service_escalation_count(递增), device_type(iOS)
    # ============================================================
    {
        "name": "收到坏的商品要退货",
        "intent": "after_sale",
        "description": "用户收到破损商品，情绪愤怒要求退货",
        "conversation": [
            {"role": "user", "content": "刚收到的手机屏幕有划痕，你们发货不检查的吗？我要退货！"},
            {"role": "assistant", "content": "非常抱歉！请问您的订单号是多少？我马上帮您核实处理。"},
            {"role": "user", "content": "ORD-20260502-002，大晚上拆快递发现这样真的很烦。上次买衣服尺码不对退了一次，这次又出问题。"},
            {"role": "assistant", "content": "查到您的订单了，确实很抱歉。帮您申请退货退款，顺丰上门取件，您看方便吗？"},
            {"role": "user", "content": "赶紧处理吧，别让我等太久。我平时都用你们APP下单的，体验一直还行，这次太差了。用iPhone买的，截图都留着呢。"},
        ],
        "expected_slots": {
            "complaint_tendency": "高",
            "satisfaction_score": 10,
            "response_patience": "低",
            "return_rate": "高",
            "channel_preference": "APP",
            "active_time": "晚间",
            "service_escalation_count": 1,
            "device_type": "iOS",
        },
    },

    # ============================================================
    # 场景4：给家里猫咪囤货
    # 自然泄露：gender(女), pet_ownership(养猫), preferred_categories(宠物用品),
    #           repurchase_intent(高), purchase_frequency(每月),
    #           avg_order_value(256), lifestyle_tags(猫奴),
    #           shopping_motivation(家用), new_vs_returning(老客),
    #           customer_lifecycle(忠诚客户), review_behavior(活跃评价者)
    # ============================================================
    {
        "name": "给家里猫咪囤货",
        "intent": "pre_sale",
        "description": "养猫用户每月固定复购猫粮猫砂",
        "conversation": [
            {"role": "user", "content": "皇家猫粮2kg的还有货吗？上个月买的快吃完了"},
            {"role": "assistant", "content": "有的，还是88元一袋。您之前买过好几次了，这次还是老规格吗？"},
            {"role": "user", "content": "对，再来两袋，再加两袋豆腐猫砂。我家两只猫一个月差不多花三百。"},
            {"role": "assistant", "content": "好的，猫粮两袋加猫砂两袋，一共256元。老顾客了，送您一包猫零食试用装。"},
            {"role": "user", "content": "谢谢，每次都在你们这买，习惯了。发货快点哈，快断粮了。收到后我给你们写个好评，上次那个猫砂确实好用。"},
        ],
        "expected_slots": {
            "gender": "女",
            "pet_ownership": "养猫",
            "preferred_categories": ["宠物用品"],
            "repurchase_intent": "高",
            "purchase_frequency": "每月",
            "avg_order_value": 256,
            "lifestyle_tags": ["猫奴"],
            "shopping_motivation": "家用",
            "new_vs_returning": "老客",
            "customer_lifecycle": "忠诚客户",
            "review_behavior": "活跃评价者",
        },
    },

    # ============================================================
    # 场景5：问能不能发到县城
    # 自然泄露：region(河南信阳), living_city_tier(三四线城市),
    #           age_range(50以上), preferred_contact_method(电话),
    #           tech_savviness(入门), price_sensitivity(高),
    #           channel_preference(网页), preferred_payment_method(货到付款),
    #           search_behavior(关键词搜索), device_type(电脑)
    # ============================================================
    {
        "name": "问能不能发到县城",
        "intent": "general",
        "description": "年纪较大的用户询问物流能否送达县城",
        "conversation": [
            {"role": "user", "content": "你们能发到县城吗？我想买那个电饭煲，不知道送不送得到"},
            {"role": "assistant", "content": "可以的，我们覆盖全国大部分县城。请问您是在哪个地区呢？我帮您确认一下配送时间。"},
            {"role": "user", "content": "河南信阳下面那个光山县。我不太会弄这些，之前让儿子帮我买的，这次想自己试试。那个电饭煲有没有便宜点的？"},
            {"role": "assistant", "content": "光山县可以配送，预计3-5天。有一款美的的199元，性价比很高，适合日常做饭。"},
            {"role": "user", "content": "行就这个，货到付款行不行？我不太会用手机支付，在电脑上搜了半天才找到你们。有问题能打电话问你们吗？"},
        ],
        "expected_slots": {
            "region": "河南信阳",
            "living_city_tier": "三四线城市",
            "age_range": "50以上",
            "preferred_contact_method": "电话",
            "tech_savviness": "入门",
            "price_sensitivity": "高",
            "channel_preference": "网页",
            "preferred_payment_method": "货到付款",
            "search_behavior": "关键词搜索",
            "device_type": "电脑",
        },
    },

    # ============================================================
    # 场景6：问会员有没有专属优惠
    # 自然泄露：membership_level(钻石会员), brand_consciousness(注重品牌),
    #           hobbies(旅行/摄影), satisfaction_score(高),
    #           preferred_contact_method(在线客服), occupation(市场公关),
    #           income_level(高), consumption_level(高),
    #           lifestyle_tags(时尚达人/旅行者), promotion_sensitivity(不敏感),
    #           customer_lifecycle(活跃客户), browse_preference(按品牌浏览)
    # ============================================================
    {
        "name": "问会员有没有专属优惠",
        "intent": "general",
        "description": "高等级会员询问专属折扣和权益",
        "conversation": [
            {"role": "user", "content": "我看我是钻石会员了，最近有什么专属活动吗？"},
            {"role": "assistant", "content": "钻石会员您好！目前有会员日专享9折，还有积分兑换礼品的活动。您平时消费记录很好呢！"},
            {"role": "user", "content": "那帮我看看旅行箱和墨镜有没有折扣，下个月去日本玩。我买东西比较挑品牌，质量好就行，价格无所谓。"},
            {"role": "assistant", "content": "新秀丽旅行箱会员价85折，雷朋墨镜9折。都是大牌，品质有保障。"},
            {"role": "user", "content": "不错，两个都要了。你们客服回复挺快的，体验不错。对了帮我看看有没有适合拍照的装备，我经常在社交平台分享。平时逛你们APP都是直接搜品牌看。"},
        ],
        "expected_slots": {
            "membership_level": "钻石会员",
            "brand_consciousness": "注重品牌",
            "hobbies": ["旅行", "摄影"],
            "satisfaction_score": 80,
            "preferred_contact_method": "在线客服",
            "occupation": "市场公关",
            "income_level": "高",
            "consumption_level": "高",
            "lifestyle_tags": ["时尚达人", "旅行者"],
            "promotion_sensitivity": "不敏感",
            "customer_lifecycle": "活跃客户",
            "browse_preference": "按品牌浏览",
        },
    },

    # ============================================================
    # 场景7：给孩子买学习平板
    # 自然泄露：has_children(是), gender(女), age_range(30-40),
    #           marital_status(已婚), shopping_motivation(家用),
    #           preferred_categories(数码), decision_cycle(长),
    #           price_sensitivity(中), occupation(教师),
    #           search_behavior(筛选搜索), review_behavior(偶尔评价)
    # ============================================================
    {
        "name": "给孩子买学习平板",
        "intent": "pre_sale",
        "description": "家长想给上小学的孩子买学习平板，比较谨慎",
        "conversation": [
            {"role": "user", "content": "想给上小学的儿子买个学习平板，有没有护眼效果好一点的？"},
            {"role": "assistant", "content": "有的，步步高和科大讯飞都有专门的学生平板，通过了莱茵护眼认证。孩子上几年级呢？"},
            {"role": "user", "content": "二年级，主要是怕伤眼睛。我老公说买iPad，但我觉得专业学习机更好。能对比一下吗？不急，我慢慢选。"},
            {"role": "assistant", "content": "学习机有家长管控功能，可以限制使用时长和应用。iPad娱乐性强但管控弱。您预算大概多少？"},
            {"role": "user", "content": "两三千吧，主要是学习用。我是当老师的，比较看重内容质量。有没有同步教材的？我筛选了好几个品牌了，上次买了个手表也还行，给了个好评。"},
        ],
        "expected_slots": {
            "has_children": "是",
            "gender": "女",
            "age_range": "30-40",
            "marital_status": "已婚",
            "shopping_motivation": "家用",
            "preferred_categories": ["数码"],
            "decision_cycle": "长",
            "price_sensitivity": "中",
            "occupation": "教师",
            "search_behavior": "筛选搜索",
            "review_behavior": "偶尔评价",
        },
    },

    # ============================================================
    # 场景8：健身达人买蛋白粉
    # 自然泄露：hobbies(健身), gender(男), age_range(25-30),
    #           shopping_motivation(自用), preferred_categories(运动),
    #           brand_affinity(肌肉科技), repurchase_intent(高),
    #           purchase_frequency(每月), lifestyle_tags(健身控),
    #           new_vs_returning(老客), customer_lifecycle(忠诚客户)
    # ============================================================
    {
        "name": "健身达人买蛋白粉",
        "intent": "pre_sale",
        "description": "健身爱好者定期购买蛋白粉和运动补剂",
        "conversation": [
            {"role": "user", "content": "肌肉科技的乳清蛋白粉5磅的还有吗？上次买的喝完了"},
            {"role": "assistant", "content": "有的，巧克力味和香草味都有货。您之前买过好几次了，还是老口味吗？"},
            {"role": "user", "content": "巧克力吧，再来一桶。我一周练五次，消耗快。对了你们那个运动背心有没有大码的？"},
            {"role": "assistant", "content": "有的，最大到3XL。蛋白粉加背心一共488元，老顾客95折。"},
            {"role": "user", "content": "行，下单吧。每次练完喝一杯，效果确实好，一直回购的。你们家蛋白粉我买了快两年了。"},
        ],
        "expected_slots": {
            "hobbies": ["健身"],
            "gender": "男",
            "age_range": "25-30",
            "shopping_motivation": "自用",
            "preferred_categories": ["运动"],
            "brand_affinity": ["肌肉科技"],
            "repurchase_intent": "高",
            "purchase_frequency": "每月",
            "lifestyle_tags": ["健身控"],
            "new_vs_returning": "老客",
            "customer_lifecycle": "忠诚客户",
        },
    },
]

# ============================================================
# 槽位覆盖汇总（40槽位，按价值排序）
# ============================================================
COVERAGE_SUMMARY = {
    "基础画像": {
        "gender": {
            "覆盖场景": ["场景1", "场景2", "场景4", "场景7", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "老婆/老公/男朋友/女朋友/儿子/女儿 等称呼直接推断",
        },
        "age_range": {
            "覆盖场景": ["场景2", "场景5", "场景7", "场景8"],
            "捕获难度": "中",
            "自然泄露方式": "学生→20-25, 不会手机支付→50+, 孩子上小学→30-40, 健身→25-30",
        },
        "region": {
            "覆盖场景": ["场景1", "场景5"],
            "捕获难度": "低",
            "自然泄露方式": "发上海浦东、河南信阳光山县 等收货地址",
        },
        "income_level": {
            "覆盖场景": ["场景1", "场景2", "场景6"],
            "捕获难度": "中",
            "自然泄露方式": "预算一千→中高, 两百以内→低, 价格无所谓→高",
        },
        "occupation": {
            "覆盖场景": ["场景6", "场景7"],
            "捕获难度": "中",
            "自然泄露方式": "做市场的经常出差、我是当老师的 等语境透露",
        },
        "marital_status": {
            "覆盖场景": ["场景1", "场景7"],
            "捕获难度": "低",
            "自然泄露方式": "老婆/我老公说 直接推断已婚",
        },
        "has_children": {
            "覆盖场景": ["场景7"],
            "捕获难度": "低",
            "自然泄露方式": "给上小学的儿子买→有孩子",
        },
        "living_city_tier": {
            "覆盖场景": ["场景1", "场景5"],
            "捕获难度": "中",
            "自然泄露方式": "上海浦东→一线, 光山县→三四线",
        },
    },
    "消费特征": {
        "price_sensitivity": {
            "覆盖场景": ["场景1", "场景2", "场景5", "场景7"],
            "捕获难度": "低",
            "自然泄露方式": "有没有便宜点的→高, 别太便宜拿不出手→中, 价格无所谓→低",
        },
        "preferred_categories": {
            "覆盖场景": ["场景1", "场景2", "场景4", "场景7", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "买什么品类直接体现偏好",
        },
        "shopping_motivation": {
            "覆盖场景": ["场景1", "场景4", "场景7", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "送老婆→送礼, 自己喝→自用, 给儿子→家用",
        },
        "consumption_level": {
            "覆盖场景": ["场景1", "场景2", "场景6"],
            "捕获难度": "中",
            "自然泄露方式": "由客单价和购买频次综合推断",
        },
        "brand_affinity": {
            "覆盖场景": ["场景1", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "一直用雅诗兰黛、肌肉科技→品牌偏好",
        },
        "decision_cycle": {
            "覆盖场景": ["场景1", "场景7"],
            "捕获难度": "中",
            "自然泄露方式": "生日快到了→短, 不急慢慢选→长",
        },
        "avg_order_value": {
            "覆盖场景": ["场景4"],
            "捕获难度": "中",
            "自然泄露方式": "一个月差不多花三百→需多轮积累取均值",
        },
        "purchase_frequency": {
            "覆盖场景": ["场景4", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "每月都来买、一周练五次消耗快→高频",
        },
        "repurchase_intent": {
            "覆盖场景": ["场景4", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "上个月买的快吃完了、一直回购→高复购",
        },
        "preferred_payment_method": {
            "覆盖场景": ["场景2", "场景5"],
            "捕获难度": "低",
            "自然泄露方式": "花呗/支付宝/货到付款 直接体现",
        },
        "coupon_usage_rate": {
            "覆盖场景": ["场景2"],
            "捕获难度": "低",
            "自然泄露方式": "有券就好、买东西都先看有没有券→高",
        },
        "promotion_sensitivity": {
            "覆盖场景": ["场景2", "场景6"],
            "捕获难度": "中",
            "自然泄露方式": "先看有没有券→非常敏感, 价格无所谓→不敏感",
        },
    },
    "服务交互": {
        "satisfaction_score": {
            "覆盖场景": ["场景3", "场景6"],
            "捕获难度": "中",
            "自然泄露方式": "由情绪+投诉次数综合计算",
        },
        "complaint_tendency": {
            "覆盖场景": ["场景3"],
            "捕获难度": "中",
            "自然泄露方式": "直接投诉+提及之前也退过→高投诉倾向",
        },
        "membership_level": {
            "覆盖场景": ["场景6"],
            "捕获难度": "低",
            "自然泄露方式": "我是钻石会员→直接获取",
        },
        "channel_preference": {
            "覆盖场景": ["场景3", "场景5"],
            "捕获难度": "低",
            "自然泄露方式": "用APP下单、在电脑上搜→网页",
        },
        "device_type": {
            "覆盖场景": ["场景3", "场景5"],
            "捕获难度": "低",
            "自然泄露方式": "用iPhone买的→iOS, 在电脑上搜→电脑",
        },
        "active_time": {
            "覆盖场景": ["场景3"],
            "捕获难度": "低",
            "自然泄露方式": "大晚上拆快递→晚间活跃",
        },
        "preferred_contact_method": {
            "覆盖场景": ["场景5", "场景6"],
            "捕获难度": "低",
            "自然泄露方式": "有问题能打电话问吗→电话, 客服回复挺快→在线",
        },
        "response_patience": {
            "覆盖场景": ["场景3"],
            "捕获难度": "中",
            "自然泄露方式": "赶紧处理别让我等太久→低耐心",
        },
    },
    "兴趣生活": {
        "hobbies": {
            "覆盖场景": ["场景2", "场景6", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "打游戏/健身/旅行拍照→直接体现",
        },
        "lifestyle_tags": {
            "覆盖场景": ["场景4", "场景6", "场景8"],
            "捕获难度": "中",
            "自然泄露方式": "猫奴/时尚达人/健身控/旅行者 由行为推断",
        },
        "brand_consciousness": {
            "覆盖场景": ["场景6"],
            "捕获难度": "中",
            "自然泄露方式": "比较挑品牌、质量好就行→注重品牌",
        },
        "tech_savviness": {
            "覆盖场景": ["场景2", "场景5"],
            "捕获难度": "中",
            "自然泄露方式": "打游戏选低延迟耳机→数码达人, 不会手机支付→入门",
        },
        "pet_ownership": {
            "覆盖场景": ["场景4"],
            "捕获难度": "低",
            "自然泄露方式": "买猫粮猫砂→养猫, 直接体现",
        },
        "new_vs_returning": {
            "覆盖场景": ["场景1", "场景2", "场景4", "场景8"],
            "捕获难度": "低",
            "自然泄露方式": "之前买过几次→老客, 第一次来→新客",
        },
    },
    "行为特征": {
        "browse_preference": {
            "覆盖场景": ["场景2", "场景6"],
            "捕获难度": "中",
            "自然泄露方式": "按价格从低到高排→按价格排序, 直接搜品牌→按品牌浏览",
        },
        "search_behavior": {
            "覆盖场景": ["场景5", "场景7"],
            "捕获难度": "中",
            "自然泄露方式": "搜了半天才找到→关键词搜索, 筛选了好几个品牌→筛选搜索",
        },
        "review_behavior": {
            "覆盖场景": ["场景4", "场景7"],
            "捕获难度": "中",
            "自然泄露方式": "给你们写个好评→活跃评价者, 上次给了个好评→偶尔评价",
        },
        "customer_lifecycle": {
            "覆盖场景": ["场景4", "场景6", "场景8"],
            "捕获难度": "中",
            "自然泄露方式": "买了快两年→忠诚客户, 消费记录很好→活跃客户",
        },
        "return_rate": {
            "覆盖场景": ["场景3"],
            "捕获难度": "中",
            "自然泄露方式": "上次退了一次这次又出问题→需多轮积累",
        },
        "service_escalation_count": {
            "覆盖场景": ["场景3"],
            "捕获难度": "中",
            "自然泄露方式": "投诉时递增，需跨会话累计",
        },
    },
}


def print_coverage_check():
    """打印槽位覆盖检查结果"""
    all_slots = set()
    for category, slots in COVERAGE_SUMMARY.items():
        for slot_name in slots:
            all_slots.add(slot_name)

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
    from config import DEFAULT_USER_PROFILE
    config_slots = set(DEFAULT_USER_PROFILE.keys())
    missing = config_slots - all_slots
    extra = all_slots - config_slots

    print(f"\n总槽位数: {len(all_slots)}")
    print(f"预期40个，实际覆盖: {len(all_slots)}个")

    if missing:
        print(f"未覆盖的槽位({len(missing)}): {missing}")
    if extra:
        print(f"多余的槽位({len(extra)}): {extra}")
    if not missing and not extra:
        print("全部40个槽位已覆盖!")

    high_difficulty = []
    for cat, slots in COVERAGE_SUMMARY.items():
        for name, info in slots.items():
            if isinstance(info, dict) and info.get("捕获难度") == "高":
                high_difficulty.append(f"  [高] {cat}/{name}: {info.get('自然泄露方式', '')}")

    if high_difficulty:
        print(f"\n高难度槽位({len(high_difficulty)}个):")
        for item in high_difficulty:
            print(item)
    else:
        print("\n无高难度槽位，所有槽位均可自然捕获!")


if __name__ == "__main__":
    print("=" * 60)
    print("用户画像槽位测试用例（自然对话版 - 40槽位）")
    print("=" * 60)
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n{'='*60}")
        print(f"[场景{i}] {case['name']}")
        print(f"意图: {case['intent']}")
        print(f"描述: {case['description']}")
        print(f"对话轮次: {len(case['conversation'])}轮")
        print(f"覆盖槽位: {len(case['expected_slots'])}个")
        print(f"{'='*60}")
        for msg in case['conversation']:
            if msg['role'] == 'user':
                print(f"  用户: {msg['content']}")

    print("\n\n")
    print_coverage_check()
