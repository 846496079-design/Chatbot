MOCK_PRODUCTS = [
    {"product_id": "PROD-001", "name": "iPhone 16 Pro Max 256GB", "category": "数码", "sub_category": "手机", "brand": "Apple", "price": 9999, "original_price": 9999, "stock": "有货", "sales": 15234, "rating": 4.9, "specs": "A18芯片/8GB/256GB/6.9英寸", "selling_point": "最强A18芯片，专业级摄像系统", "target_audience": "数码发烧友/商务人士", "promotion": "暂无优惠", "description": "最新款旗舰手机，A18芯片，4800万像素摄像头", "features": ["6.9英寸屏幕", "256GB存储", "钛金属边框"]},
    {"product_id": "PROD-002", "name": "华为Mate 70 Pro 512GB", "category": "数码", "sub_category": "手机", "brand": "华为", "price": 6999, "original_price": 7999, "stock": "有货", "sales": 8921, "rating": 4.8, "specs": "麒麟9100/12GB/512GB/6.8英寸", "selling_point": "卫星通信，XMAGE影像", "target_audience": "商务人士/摄影爱好者", "promotion": "限时降1000元", "description": "国产旗舰，麒麟芯片，卫星通信", "features": ["6.8英寸屏幕", "512GB存储", "卫星通话"]},
    {"product_id": "PROD-003", "name": "MacBook Air M4 13英寸", "category": "数码", "sub_category": "笔记本", "brand": "Apple", "price": 8999, "original_price": 9499, "stock": "有货", "sales": 4567, "rating": 4.9, "specs": "M4芯片/16GB/256GB/13.6英寸", "selling_point": "M4芯片性能飞跃，18小时续航", "target_audience": "学生/设计师/程序员", "promotion": "教育优惠减500", "description": "轻薄笔记本，M4芯片，18小时续航", "features": ["13.6英寸", "16GB内存", "256GB存储"]},
    {"product_id": "PROD-004", "name": "索尼WH-1000XM6头戴耳机", "category": "数码", "sub_category": "耳机", "brand": "索尼", "price": 2499, "original_price": 2999, "stock": "有货", "sales": 12340, "rating": 4.7, "specs": "蓝牙5.3/30h续航/主动降噪", "selling_point": "旗舰降噪，Hi-Res音质", "target_audience": "音乐爱好者/通勤族", "promotion": "618特价2499", "description": "旗舰降噪耳机，30小时续航", "features": ["主动降噪", "蓝牙5.3", "30小时续航"]},
    {"product_id": "PROD-005", "name": "iPad Pro M4 11英寸", "category": "数码", "sub_category": "平板", "brand": "Apple", "price": 6799, "original_price": 6799, "stock": "有货", "sales": 6789, "rating": 4.8, "specs": "M4芯片/8GB/128GB/11英寸", "selling_point": "轻薄便携，Apple Pencil Pro", "target_audience": "学生/设计师/画师", "promotion": "暂无优惠", "description": "专业级平板，M4芯片，支持Apple Pencil", "features": ["11英寸", "128GB存储", "120Hz刷新率"]},
    {"product_id": "PROD-006", "name": "男士商务休闲夹克", "category": "服装", "sub_category": "男装", "brand": "海澜之家", "price": 599, "original_price": 899, "stock": "有货", "sales": 3456, "rating": 4.5, "specs": "棉质/商务休闲/多色可选", "selling_point": "免烫抗皱，商务百搭", "target_audience": "25-45岁职场男性", "promotion": "满299减50", "description": "春秋季商务休闲夹克，修身版型", "features": ["棉质面料", "多色可选", "M-3XL"]},
    {"product_id": "PROD-007", "name": "女士碎花连衣裙夏季新款", "category": "服装", "sub_category": "女装", "brand": "伊芙丽", "price": 399, "original_price": 599, "stock": "少量", "sales": 5678, "rating": 4.6, "specs": "雪纺/碎花/V领/中长款", "selling_point": "法式复古风，透气亲肤", "target_audience": "20-35岁女性", "promotion": "2件8折", "description": "法式复古碎花连衣裙，透气面料", "features": ["雪纺面料", "S-XL", "多色可选"]},
    {"product_id": "PROD-008", "name": "Nike Air Max 运动跑鞋", "category": "服装", "sub_category": "运动鞋", "brand": "Nike", "price": 899, "original_price": 1099, "stock": "有货", "sales": 9876, "rating": 4.7, "specs": "网面/气垫/橡胶底", "selling_point": "Air Max气垫，舒适缓震", "target_audience": "运动爱好者/年轻人", "promotion": "满899减100", "description": "Air Zoom缓震跑鞋，轻量透气", "features": ["网面材质", "38-45码", "黑白配色"]},
    {"product_id": "PROD-009", "name": "波司登轻薄羽绒服", "category": "服装", "sub_category": "羽绒服", "brand": "波司登", "price": 1299, "original_price": 1699, "stock": "有货", "sales": 2345, "rating": 4.8, "specs": "90%白鹅绒/轻薄款", "selling_point": "轻暖科技，可收纳", "target_audience": "全年龄段", "promotion": "反季特价", "description": "90%白鹅绒填充，防风保暖", "features": ["鹅绒填充", "防风面料", "可拆卸帽"]},
    {"product_id": "PROD-010", "name": "万事利100%真丝围巾", "category": "服装", "sub_category": "配饰", "brand": "万事利", "price": 299, "original_price": 399, "stock": "有货", "sales": 1234, "rating": 4.6, "specs": "100%桑蚕丝/手工卷边", "selling_point": "杭州老字号，送礼佳品", "target_audience": "女性/送礼人群", "promotion": "满2件包邮", "description": "100%桑蚕丝，手工卷边", "features": ["桑蚕丝", "多色可选", "礼盒包装"]},
    {"product_id": "PROD-011", "name": "科沃斯X2智能扫地机器人", "category": "家居", "sub_category": "清洁电器", "brand": "科沃斯", "price": 3299, "original_price": 4299, "stock": "有货", "sales": 7890, "rating": 4.7, "specs": "激光导航/5000Pa/自动集尘", "selling_point": "全能扫拖，AI避障", "target_audience": "家庭用户/养宠家庭", "promotion": "以旧换新减300", "description": "激光导航，扫拖一体，自动集尘", "features": ["激光导航", "5000Pa吸力", "自动回充"]},
    {"product_id": "PROD-012", "name": "小米空气净化器Pro", "category": "家居", "sub_category": "生活电器", "brand": "小米", "price": 1999, "original_price": 2499, "stock": "有货", "sales": 12345, "rating": 4.6, "specs": "CADR 500m³/h/OLED触屏", "selling_point": "除甲醛/除菌/静音", "target_audience": "新装修家庭/母婴家庭", "promotion": "618直降500", "description": "除甲醛雾霾，CADR值500m³/h", "features": ["HEPA滤网", "智能联动", "静音模式"]},
    {"product_id": "PROD-013", "name": "邓禄普天然乳胶枕头", "category": "家居", "sub_category": "床上用品", "brand": "邓禄普", "price": 399, "original_price": 599, "stock": "有货", "sales": 6789, "rating": 4.5, "specs": "天然乳胶/人体工学/透气", "selling_point": "泰国进口乳胶，护颈助眠", "target_audience": "颈椎不适人群/上班族", "promotion": "买一送枕套", "description": "天然乳胶，人体工学设计", "features": ["天然乳胶", "透气防螨", "高低可选"]},
    {"product_id": "PROD-014", "name": "德施曼Q50智能门锁", "category": "家居", "sub_category": "智能家居", "brand": "德施曼", "price": 1599, "original_price": 1999, "stock": "有货", "sales": 4567, "rating": 4.7, "specs": "3D人脸识别/指纹/远程", "selling_point": "七种开锁方式，金融级安全", "target_audience": "家庭用户/独居女性", "promotion": "包安装", "description": "指纹密码锁，支持远程开锁", "features": ["指纹识别", "密码开锁", "APP远程"]},
    {"product_id": "PROD-015", "name": "水星家纺100%蚕丝被", "category": "家居", "sub_category": "床上用品", "brand": "水星家纺", "price": 899, "original_price": 1299, "stock": "有货", "sales": 3456, "rating": 4.6, "specs": "100%桑蚕丝/2斤/四季通用", "selling_point": "亲肤透气，恒温舒适", "target_audience": "注重睡眠品质人群", "promotion": "满899减100", "description": "100%桑蚕丝，四季通用", "features": ["桑蚕丝", "2斤/4斤可选", "可水洗"]},
    {"product_id": "PROD-016", "name": "兰蔻小黑瓶精华液50ml", "category": "美妆", "sub_category": "护肤", "brand": "兰蔻", "price": 1280, "original_price": 1580, "stock": "有货", "sales": 8901, "rating": 4.8, "specs": "二裂酵母/修护/抗初老", "selling_point": "7天修护肌肤屏障", "target_audience": "25-45岁女性", "promotion": "赠同款小样", "description": "小黑瓶精华肌底液+眼霜套装", "features": ["50ml精华", "修护抗老", "礼盒装"]},
    {"product_id": "PROD-017", "name": "安热沙小金瓶防晒霜60ml", "category": "美妆", "sub_category": "护肤", "brand": "安热沙", "price": 198, "original_price": 258, "stock": "有货", "sales": 15678, "rating": 4.7, "specs": "SPF50+/PA++++/防水", "selling_point": "清爽不油腻，军训必备", "target_audience": "全年龄段/户外人群", "promotion": "2件9折", "description": "SPF50+ PA++++，清爽不油腻", "features": ["60ml", "防水防汗", "敏感肌可用"]},
    {"product_id": "PROD-018", "name": "MAC子弹头口红套装3支", "category": "美妆", "sub_category": "彩妆", "brand": "MAC", "price": 360, "original_price": 480, "stock": "有货", "sales": 6789, "rating": 4.6, "specs": "哑光/滋润/3色套装", "selling_point": "经典色号，不挑肤色", "target_audience": "18-35岁女性", "promotion": "赠化妆包", "description": "经典子弹头口红3支套装", "features": ["3支装", "热门色号", "哑光质地"]},
    {"product_id": "PROD-019", "name": "雅诗兰黛DW持妆粉底液", "category": "美妆", "sub_category": "彩妆", "brand": "雅诗兰黛", "price": 480, "original_price": 580, "stock": "少量", "sales": 5678, "rating": 4.7, "specs": "SPF10/控油/遮瑕/30ml", "selling_point": "油皮亲妈，24h持妆", "target_audience": "油性/混油肌肤", "promotion": "暂无优惠", "description": "DW持妆粉底液，控油遮瑕", "features": ["30ml", "多色号", "24小时持妆"]},
    {"product_id": "PROD-020", "name": "迪奥真我香水礼盒50ml", "category": "美妆", "sub_category": "香水", "brand": "迪奥", "price": 880, "original_price": 1080, "stock": "有货", "sales": 3456, "rating": 4.8, "specs": "花香调/50ml/EDP", "selling_point": "经典真我系列，优雅持久", "target_audience": "25-45岁女性/送礼", "promotion": "赠香水小样", "description": "真我香水50ml+身体乳套装", "features": ["50ml香水", "身体乳", "礼盒装"]},
    {"product_id": "PROD-021", "name": "三只松鼠坚果大礼包1888g", "category": "食品", "sub_category": "零食", "brand": "三只松鼠", "price": 128, "original_price": 188, "stock": "有货", "sales": 25678, "rating": 4.7, "specs": "8袋装/混合坚果", "selling_point": "年货爆款，独立小包装", "target_audience": "全年龄段/送礼", "promotion": "满199减30", "description": "8袋混合坚果大礼包，独立小包装", "features": ["8袋装", "混合坚果", "礼盒包装"]},
    {"product_id": "PROD-022", "name": "认养一头牛纯牛奶250ml*24盒", "category": "食品", "sub_category": "乳品", "brand": "认养一头牛", "price": 79, "original_price": 99, "stock": "有货", "sales": 34567, "rating": 4.8, "specs": "250ml*24盒", "selling_point": "自有牧场，3.6g优质乳蛋白", "target_audience": "家庭/儿童/老人", "promotion": "2箱9折", "description": "纯牛奶整箱，自有牧场奶源", "features": ["250ml*24盒", "3.6g乳蛋白", "整箱装"]},
    {"product_id": "PROD-023", "name": "良品铺子零食大礼包30袋", "category": "食品", "sub_category": "零食", "brand": "良品铺子", "price": 99, "original_price": 139, "stock": "有货", "sales": 18900, "rating": 4.6, "specs": "30袋/混合口味", "selling_point": "追剧必备，30种不重样", "target_audience": "年轻人/学生", "promotion": "满99减15", "description": "30袋混合零食大礼包，多种口味", "features": ["30袋装", "混合口味", "独立包装"]},
    {"product_id": "PROD-024", "name": "五粮液普五第八代500ml", "category": "食品", "sub_category": "酒类", "brand": "五粮液", "price": 1299, "original_price": 1499, "stock": "少量", "sales": 3456, "rating": 4.9, "specs": "52度/500ml", "selling_point": "浓香经典，送礼首选", "target_audience": "商务人士/送礼", "promotion": "赠礼品袋", "description": "五粮液普五第八代，浓香型白酒", "features": ["52度", "500ml", "浓香型"]},
    {"product_id": "PROD-025", "name": "德芙巧克力礼盒装588g", "category": "食品", "sub_category": "零食", "brand": "德芙", "price": 89, "original_price": 119, "stock": "有货", "sales": 23456, "rating": 4.7, "specs": "588g/多口味", "selling_point": "丝滑口感，节日送礼", "target_audience": "女性/情侣/送礼", "promotion": "2件8折", "description": "德芙巧克力礼盒，多口味组合", "features": ["588g", "多口味", "礼盒装"]},
    {"product_id": "PROD-026", "name": "花王妙而舒纸尿裤L54片*4包", "category": "母婴", "sub_category": "纸尿裤", "brand": "花王", "price": 299, "original_price": 399, "stock": "有货", "sales": 15678, "rating": 4.8, "specs": "L码/54片*4包", "selling_point": "日本进口，透气干爽", "target_audience": "0-2岁宝宝家长", "promotion": "满499减80", "description": "花王妙而舒纸尿裤，日本进口", "features": ["L码", "54片*4包", "透气干爽"]},
    {"product_id": "PROD-027", "name": "飞鹤星飞帆3段奶粉900g*2罐", "category": "母婴", "sub_category": "奶粉", "brand": "飞鹤", "price": 498, "original_price": 598, "stock": "有货", "sales": 8900, "rating": 4.9, "specs": "3段/900g*2罐", "selling_point": "更适合中国宝宝体质", "target_audience": "1-3岁宝宝家长", "promotion": "赠儿童餐具", "description": "飞鹤星飞帆3段婴幼儿配方奶粉", "features": ["3段", "900g*2罐", "适合1-3岁"]},
    {"product_id": "PROD-028", "name": "babycare婴儿湿巾80抽*12包", "category": "母婴", "sub_category": "护理", "brand": "babycare", "price": 89, "original_price": 119, "stock": "有货", "sales": 23456, "rating": 4.7, "specs": "80抽*12包", "selling_point": "EDI纯水，手口可用", "target_audience": "0-3岁宝宝家长", "promotion": "满199减30", "description": "babycare婴儿手口湿巾，EDI纯水", "features": ["80抽*12包", "手口可用", "无添加"]},
    {"product_id": "PROD-029", "name": "好孩子婴儿推车轻便折叠", "category": "母婴", "sub_category": "推车", "brand": "好孩子", "price": 899, "original_price": 1199, "stock": "有货", "sales": 5678, "rating": 4.6, "specs": "轻便款/可坐可躺", "selling_point": "一键折叠，可上飞机", "target_audience": "0-3岁宝宝家长", "promotion": "618直降300", "description": "好孩子轻便折叠婴儿推车", "features": ["轻便折叠", "可坐可躺", "可上飞机"]},
    {"product_id": "PROD-030", "name": "贝亲宽口径玻璃奶瓶240ml", "category": "母婴", "sub_category": "喂养", "brand": "贝亲", "price": 99, "original_price": 129, "stock": "有货", "sales": 18900, "rating": 4.8, "specs": "240ml/玻璃", "selling_point": "日本品牌，仿母乳设计", "target_audience": "0-1岁宝宝家长", "promotion": "2件9折", "description": "贝亲宽口径玻璃奶瓶，仿母乳实感", "features": ["240ml", "玻璃材质", "宽口径"]},
    {"product_id": "PROD-031", "name": "李宁超轻21代跑鞋", "category": "运动", "sub_category": "跑鞋", "brand": "李宁", "price": 499, "original_price": 599, "stock": "有货", "sales": 12345, "rating": 4.7, "specs": "男女同款/多色", "selling_point": "超轻科技，回弹出色", "target_audience": "跑步爱好者", "promotion": "满499减50", "description": "李宁超轻21代跑鞋，轻量回弹", "features": ["超轻科技", "男女同款", "多色可选"]},
    {"product_id": "PROD-032", "name": "迪卡侬椭圆机EL520", "category": "运动", "sub_category": "器械", "brand": "迪卡侬", "price": 2499, "original_price": 2999, "stock": "有货", "sales": 3456, "rating": 4.5, "specs": "家用静音款", "selling_point": "静音磁控，APP智联", "target_audience": "家庭健身人群", "promotion": "包安装", "description": "迪卡侬家用静音椭圆机，磁控阻力", "features": ["静音磁控", "APP智联", "家用款"]},
    {"product_id": "PROD-033", "name": "Keep智能计数跳绳", "category": "运动", "sub_category": "小器械", "brand": "Keep", "price": 79, "original_price": 99, "stock": "有货", "sales": 23456, "rating": 4.6, "specs": "蓝牙连接/APP同步", "selling_point": "精准计数，运动数据同步", "target_audience": "健身入门/学生", "promotion": "暂无优惠", "description": "Keep智能计数跳绳，蓝牙连接APP", "features": ["蓝牙连接", "APP同步", "精准计数"]},
    {"product_id": "PROD-034", "name": "尤尼克斯羽毛球拍天斧99", "category": "运动", "sub_category": "球拍", "brand": "尤尼克斯", "price": 899, "original_price": 1099, "stock": "少量", "sales": 4567, "rating": 4.8, "specs": "4U/进攻型", "selling_point": "日本进口，杀球利器", "target_audience": "羽毛球爱好者", "promotion": "赠拍套+手胶", "description": "尤尼克斯天斧99羽毛球拍，进攻型", "features": ["4U重量", "进攻型", "日本进口"]},
    {"product_id": "PROD-035", "name": "骆驼户外冲锋衣男女三合一", "category": "运动", "sub_category": "户外服装", "brand": "骆驼", "price": 599, "original_price": 899, "stock": "有货", "sales": 8900, "rating": 4.6, "specs": "男女款/多色", "selling_point": "防风防水透气，可拆卸内胆", "target_audience": "户外爱好者", "promotion": "反季特价", "description": "骆驼三合一冲锋衣，防风防水透气", "features": ["防风防水", "可拆卸内胆", "男女同款"]},
    {"product_id": "PROD-036", "name": "三体全集(全3册)", "category": "图书", "sub_category": "科幻", "brand": "刘慈欣", "price": 68, "original_price": 99, "stock": "有货", "sales": 56789, "rating": 4.9, "specs": "平装/3册", "selling_point": "雨果奖获奖作品，科幻必读", "target_audience": "科幻爱好者/学生", "promotion": "满100减20", "description": "三体全集，刘慈欣科幻巨著", "features": ["全3册", "平装", "雨果奖作品"]},
    {"product_id": "PROD-037", "name": "原则：应对变化中的世界秩序", "category": "图书", "sub_category": "经管", "brand": "瑞·达利欧", "price": 89, "original_price": 129, "stock": "有货", "sales": 23456, "rating": 4.7, "specs": "精装/单册", "selling_point": "桥水基金创始人新作", "target_audience": "职场人士/管理者", "promotion": "暂无优惠", "description": "原则2，瑞·达利欧关于世界秩序的新作", "features": ["精装", "单册", "经管类"]},
    {"product_id": "PROD-038", "name": "蛤蟆先生去看心理医生", "category": "图书", "sub_category": "心理", "brand": "罗伯特·戴博德", "price": 38, "original_price": 48, "stock": "有货", "sales": 34567, "rating": 4.8, "specs": "平装/单册", "selling_point": "国民心理入门书", "target_audience": "全年龄段", "promotion": "满99减15", "description": "蛤蟆先生去看心理医生，心理自助经典", "features": ["平装", "单册", "心理自助"]},
    {"product_id": "PROD-039", "name": "置身事内：中国政府与经济发展", "category": "图书", "sub_category": "社科", "brand": "兰小欢", "price": 49, "original_price": 65, "stock": "有货", "sales": 45678, "rating": 4.8, "specs": "平装/单册", "selling_point": "理解中国经济的必读之作", "target_audience": "学生/职场人士", "promotion": "暂无优惠", "description": "置身事内，理解中国政府与经济发展", "features": ["平装", "单册", "社科类"]},
    {"product_id": "PROD-040", "name": "小羊上山儿童汉语分级读物第1级", "category": "图书", "sub_category": "童书", "brand": "孙蓓", "price": 89, "original_price": 128, "stock": "有货", "sales": 12345, "rating": 4.9, "specs": "10册套装", "selling_point": "零基础识字，幼小衔接", "target_audience": "3-6岁儿童家长", "promotion": "满199减30", "description": "小羊上山第1级，儿童汉语分级读物", "features": ["10册套装", "零基础识字", "幼小衔接"]},
]


def search_products(category=None, brand=None, min_price=None, max_price=None, keyword=None):
    """根据条件检索商品"""
    results = MOCK_PRODUCTS
    if category:
        results = [p for p in results if p["category"] == category or p.get("sub_category") == category]
    if brand:
        results = [p for p in results if brand.lower() in p["brand"].lower()]
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]
    if keyword:
        keyword_lower = keyword.lower()
        results = [p for p in results if keyword_lower in p["name"].lower() or keyword_lower in p.get("description", "").lower() or keyword_lower in p["category"].lower()]
    return results


def get_product_by_id(product_id):
    """根据ID获取商品"""
    for p in MOCK_PRODUCTS:
        if p["product_id"] == product_id:
            return p
    return None


# 场景关键词到商品品类的映射
SCENE_KEYWORD_MAP = {
    # 睡眠场景
    "睡不着": ["床上用品"],
    "失眠": ["床上用品"],
    "睡不好": ["床上用品"],
    "颈椎": ["床上用品"],
    "枕头": ["床上用品"],
    # 噪音场景
    "吵": ["耳机"],
    "噪音": ["耳机"],
    "安静": ["耳机"],
    "降噪": ["耳机"],
    "室友": ["耳机"],
    # 送礼场景
    "送礼": ["配饰", "香水", "零食", "酒类"],
    "礼物": ["配饰", "香水", "零食", "酒类"],
    "送人": ["配饰", "香水", "零食", "酒类"],
    # 运动场景
    "跑步": ["跑鞋", "运动鞋", "小器械"],
    "健身": ["器械", "小器械", "跑鞋"],
    "减肥": ["器械", "小器械", "跑鞋"],
    # 母婴场景
    "宝宝": ["纸尿裤", "奶粉", "护理", "推车", "喂养"],
    "孩子": ["纸尿裤", "奶粉", "护理", "推车", "喂养", "童书"],
    "婴儿": ["纸尿裤", "奶粉", "护理", "推车", "喂养"],
    "怀孕": ["纸尿裤", "奶粉", "护理"],
    # 护肤场景
    "皮肤": ["护肤", "彩妆"],
    "长痘": ["护肤"],
    "防晒": ["护肤"],
    "化妆": ["彩妆", "护肤"],
    # 家居场景
    "搬家": ["清洁电器", "生活电器", "床上用品", "智能家居"],
    "新房子": ["清洁电器", "生活电器", "床上用品", "智能家居"],
    "装修": ["清洁电器", "生活电器", "床上用品", "智能家居"],
    # 学习场景
    "学习": ["平板", "手机", "笔记本", "图书"],
    "考试": ["图书", "平板"],
    "看书": ["图书", "平板"],
    # 季节场景
    "夏天": ["护肤", "女装", "运动鞋", "户外服装"],
    "热": ["护肤", "女装", "运动鞋"],
    "防晒": ["护肤"],
    "冬天": ["羽绒服", "男装", "女装", "户外服装"],
    "冷": ["羽绒服", "男装", "女装", "户外服装"],
    # 通勤场景
    "上班": ["男装", "耳机", "笔记本"],
    "通勤": ["耳机", "男装", "女装"],
    "出差": ["男装", "耳机", "笔记本"],
    # 旅游场景
    "旅游": ["户外服装", "运动鞋", "护肤"],
    "旅行": ["户外服装", "运动鞋", "护肤"],
    # 数码场景
    "手机": ["手机"],
    "电脑": ["笔记本"],
    "耳机": ["耳机"],
    "平板": ["平板"],
    # 食品场景
    "零食": ["零食"],
    "牛奶": ["乳品"],
    "酒": ["酒类"],
    "巧克力": ["零食"],
}


def recommend_by_scene(user_input: str, max_results: int = 3):
    """根据用户输入中的场景关键词推荐商品"""
    matched_categories = set()
    for keyword, categories in SCENE_KEYWORD_MAP.items():
        if keyword in user_input:
            matched_categories.update(categories)

    if not matched_categories:
        return []

    results = []
    for product in MOCK_PRODUCTS:
        if product.get("sub_category") in matched_categories or product.get("category") in matched_categories:
            results.append(product)

    # 按销量排序，取前N个
    results.sort(key=lambda x: x.get("sales", 0), reverse=True)
    return results[:max_results]
