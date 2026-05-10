MOCK_ORDERS = [
    {"order_id": "ORD-20260501-001", "product_name": "iPhone 16 Pro Max 256GB", "product_id": "PROD-001", "quantity": 1, "amount": 9999, "discount": 0, "paid_amount": 9999, "status": "已签收", "payment_method": "微信支付", "logistics": None, "order_time": "2026-05-01 10:30", "recipient": "张先生", "phone": "138****5678", "address": "北京市朝阳区望京SOHO T1 1208", "city": "北京"},
    {"order_id": "ORD-20260502-002", "product_name": "华为Mate 70 Pro 512GB", "product_id": "PROD-002", "quantity": 1, "amount": 6999, "discount": 1000, "paid_amount": 5999, "status": "运输中", "payment_method": "支付宝", "logistics": {"tracking_no": "LOG-001", "carrier": "顺丰速运", "estimated_delivery": "2026-05-08", "current": "到达北京海淀营业点，预计明日派送", "trajectory": [{"time": "2026-05-02 16:30", "location": "深圳宝安集散中心", "status": "已揽收", "detail": "顺丰速运已揽收"}, {"time": "2026-05-02 20:15", "location": "深圳宝安集散中心", "status": "运输中", "detail": "快件离开深圳，发往广州"}, {"time": "2026-05-03 02:30", "location": "广州天河集散中心", "status": "运输中", "detail": "快件到达广州中转"}, {"time": "2026-05-03 08:00", "location": "广州天河集散中心", "status": "运输中", "detail": "快件离开广州，发往武汉"}, {"time": "2026-05-04 06:45", "location": "武汉东西湖集散中心", "status": "运输中", "detail": "快件到达武汉中转"}, {"time": "2026-05-04 14:00", "location": "武汉东西湖集散中心", "status": "运输中", "detail": "快件离开武汉，发往北京"}, {"time": "2026-05-06 09:30", "location": "北京顺义集散中心", "status": "运输中", "detail": "快件到达北京，准备分拣"}, {"time": "2026-05-07 07:00", "location": "北京海淀区营业点", "status": "运输中", "detail": "快件到达海淀营业点，预计明日派送"}]}, "order_time": "2026-05-02 14:20", "recipient": "李女士", "phone": "139****1234", "address": "北京市海淀区中关村大街1号", "city": "北京"},
    {"order_id": "ORD-20260503-003", "product_name": "男士商务休闲夹克", "product_id": "PROD-006", "quantity": 2, "amount": 1198, "discount": 50, "paid_amount": 1148, "status": "待发货", "payment_method": "花呗", "logistics": None, "order_time": "2026-05-03 09:15", "recipient": "王先生", "phone": "136****7890", "address": "上海市浦东新区陆家嘴环路1000号", "city": "上海"},
    {"order_id": "ORD-20260503-004", "product_name": "科沃斯X2智能扫地机器人", "product_id": "PROD-011", "quantity": 1, "amount": 3299, "discount": 300, "paid_amount": 2999, "status": "派送中", "payment_method": "微信支付", "logistics": {"tracking_no": "LOG-002", "carrier": "京东物流", "estimated_delivery": "2026-05-07", "current": "快递员张师傅(138****9012)正在派送", "trajectory": [{"time": "2026-05-03 18:00", "location": "上海嘉定仓库", "status": "已揽收", "detail": "京东物流已揽收"}, {"time": "2026-05-04 02:00", "location": "上海青浦分拣中心", "status": "运输中", "detail": "快件离开上海，发往杭州"}, {"time": "2026-05-04 08:30", "location": "杭州萧山分拣中心", "status": "运输中", "detail": "快件到达杭州"}, {"time": "2026-05-05 06:00", "location": "杭州西湖区营业部", "status": "运输中", "detail": "快件到达西湖营业部"}, {"time": "2026-05-07 08:30", "location": "杭州西湖区", "status": "派送中", "detail": "快递员张师傅(138****9012)正在派送"}]}, "order_time": "2026-05-03 16:45", "recipient": "赵女士", "phone": "137****3456", "address": "浙江省杭州市西湖区文三路478号", "city": "杭州"},
    {"order_id": "ORD-20260504-005", "product_name": "兰蔻小黑瓶精华液50ml", "product_id": "PROD-016", "quantity": 1, "amount": 1280, "discount": 0, "paid_amount": 1280, "status": "运输中", "payment_method": "支付宝", "logistics": {"tracking_no": "LOG-003", "carrier": "中通快递", "estimated_delivery": "2026-05-09", "current": "到达上海青浦分拣中心，等待分拣", "trajectory": [{"time": "2026-05-04 13:00", "location": "北京大兴仓库", "status": "已揽收", "detail": "中通快递已揽收"}, {"time": "2026-05-04 19:00", "location": "北京大兴分拣中心", "status": "运输中", "detail": "快件离开北京，发往济南"}, {"time": "2026-05-05 10:00", "location": "济南历城分拣中心", "status": "运输中", "detail": "快件到达济南中转"}, {"time": "2026-05-06 08:00", "location": "济南历城分拣中心", "status": "运输中", "detail": "快件离开济南，发往上海"}, {"time": "2026-05-07 06:00", "location": "上海青浦分拣中心", "status": "运输中", "detail": "快件到达上海，等待分拣"}]}, "order_time": "2026-05-04 11:00", "recipient": "陈女士", "phone": "135****6789", "address": "上海市徐汇区衡山路XX号", "city": "上海"},
    {"order_id": "ORD-20260504-006", "product_name": "Nike Air Max 运动跑鞋", "product_id": "PROD-008", "quantity": 1, "amount": 899, "discount": 100, "paid_amount": 799, "status": "已签收", "payment_method": "微信支付", "logistics": None, "order_time": "2026-05-04 20:30", "recipient": "刘先生", "phone": "133****2345", "address": "广东省深圳市南山区科技园南路XX号", "city": "深圳"},
    {"order_id": "ORD-20260505-007", "product_name": "小米空气净化器Pro", "product_id": "PROD-012", "quantity": 1, "amount": 1999, "discount": 500, "paid_amount": 1499, "status": "待发货", "payment_method": "支付宝", "logistics": None, "order_time": "2026-05-05 08:00", "recipient": "周先生", "phone": "132****4567", "address": "广东省广州市天河区体育西路XX号", "city": "广州"},
    {"order_id": "ORD-20260505-008", "product_name": "水星家纺100%蚕丝被", "product_id": "PROD-015", "quantity": 1, "amount": 899, "discount": 100, "paid_amount": 799, "status": "已发货", "payment_method": "微信支付", "logistics": {"tracking_no": "LOG-004", "carrier": "圆通速递", "estimated_delivery": "2026-05-10", "current": "南通叠石桥仓库已揽收", "trajectory": [{"time": "2026-05-05 15:00", "location": "南通叠石桥仓库", "status": "已揽收", "detail": "圆通速递已揽收"}]}, "order_time": "2026-05-05 13:25", "recipient": "吴女士", "phone": "131****7890", "address": "江苏省南京市鼓楼区中山北路XX号", "city": "南京"},
    {"order_id": "ORD-20260506-009", "product_name": "MAC子弹头口红套装3支", "product_id": "PROD-018", "quantity": 1, "amount": 360, "discount": 0, "paid_amount": 360, "status": "运输中", "payment_method": "花呗", "logistics": {"tracking_no": "LOG-005", "carrier": "韵达快递", "estimated_delivery": "2026-05-11", "current": "到达广州白云分拣中心，等待分拣", "trajectory": [{"time": "2026-05-06 17:00", "location": "深圳龙华仓库", "status": "已揽收", "detail": "韵达快递已揽收"}, {"time": "2026-05-06 21:00", "location": "深圳龙华分拣中心", "status": "运输中", "detail": "快件离开深圳，发往广州"}, {"time": "2026-05-07 04:00", "location": "广州白云分拣中心", "status": "运输中", "detail": "快件到达广州，等待分拣"}]}, "order_time": "2026-05-06 15:40", "recipient": "郑女士", "phone": "130****1234", "address": "广东省广州市番禺区大学城XX路", "city": "广州"},
    {"order_id": "ORD-20260506-010", "product_name": "MacBook Air M4 13英寸", "product_id": "PROD-003", "quantity": 1, "amount": 8999, "discount": 500, "paid_amount": 8499, "status": "待付款", "payment_method": None, "logistics": None, "order_time": "2026-05-06 22:10", "recipient": "孙先生", "phone": "158****5678", "address": "四川省成都市高新区天府大道XX号", "city": "成都"},
]


def search_orders(order_id=None, phone=None, status=None):
    """根据条件检索订单"""
    results = MOCK_ORDERS
    if order_id:
        results = [o for o in results if order_id.upper() in o["order_id"].upper()]
    if phone:
        results = [o for o in results if phone in o.get("phone", "").replace("*", "")]
    if status:
        results = [o for o in results if status in o["status"]]
    return results


def get_order_by_id(order_id):
    """根据订单号精确查找"""
    for o in MOCK_ORDERS:
        if o["order_id"].upper() == order_id.upper():
            return o
    return None


def get_orders_by_phone_suffix(suffix):
    """根据手机号后4位查找订单"""
    results = []
    for o in MOCK_ORDERS:
        phone = o.get("phone", "")
        if phone.endswith(suffix):
            results.append(o)
    return results
