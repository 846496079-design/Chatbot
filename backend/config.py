import os
from dotenv import load_dotenv

load_dotenv()

KIMI_API_KEY = os.getenv("KIMI_API_KEY", "sk-your-kimi-api-key-here")
KIMI_API_BASE = os.getenv("KIMI_API_BASE", "https://api.moonshot.cn/v1")
KIMI_MODEL = os.getenv("KIMI_MODEL", "moonshot-v1-8k")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8001"))

MAX_CONTEXT_ROUNDS = 10
MAX_FALLBACK_ROUNDS = 3
MAX_EMOTION_NEGATIVE_ROUNDS = 2
RATE_LIMIT_PER_MINUTE = 10
LLM_TIMEOUT = 10
LLM_MAX_RETRIES = 2

DEFAULT_USER_PROFILE = {
    # 基础画像（8个）
    "gender": "未知",
    "age_range": "未知",
    "region": "未知",
    "income_level": "未知",
    "occupation": "未知",
    "marital_status": "未知",
    "has_children": "未知",
    "living_city_tier": "未知",
    # 消费特征（12个）
    "price_sensitivity": "未知",
    "preferred_categories": [],
    "shopping_motivation": "未知",
    "consumption_level": "未知",
    "brand_affinity": [],
    "decision_cycle": "未知",
    "avg_order_value": 0,
    "purchase_frequency": "未知",
    "repurchase_intent": "未知",
    "preferred_payment_method": "未知",
    "coupon_usage_rate": "未知",
    "promotion_sensitivity": "未知",
    # 服务交互（8个）
    "satisfaction_score": 0,
    "complaint_tendency": "未知",
    "membership_level": "未知",
    "channel_preference": "未知",
    "device_type": "未知",
    "active_time": "未知",
    "preferred_contact_method": "未知",
    "response_patience": "未知",
    # 兴趣生活（6个）
    "hobbies": [],
    "lifestyle_tags": [],
    "brand_consciousness": "未知",
    "tech_savviness": "未知",
    "pet_ownership": "未知",
    "new_vs_returning": "未知",
    # 行为特征（6个）
    "browse_preference": "未知",
    "search_behavior": "未知",
    "review_behavior": "未知",
    "customer_lifecycle": "未知",
    "return_rate": "未知",
    "service_escalation_count": 0,
}
