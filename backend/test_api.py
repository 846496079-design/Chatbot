import httpx
import asyncio
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

REALTIME_SLOTS = {
    'age_range', 'gender', 'region', 'occupation', 'income_level',
    'marital_status', 'has_children',
    'consumption_level', 'price_sensitivity', 'decision_cycle',
    'preferred_categories', 'brand_affinity',
    'complaint_tendency',
    'hobbies', 'lifestyle_tags', 'shopping_motivation', 'pet_ownership',
}


async def test():
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BASE_URL}/api/session/create")
        data = r.json()
        print("Create session:", data["code"])
        session_id = data["data"]["session_id"]

        r = await c.post(f"{BASE_URL}/api/chat/send", json={
            "session_id": session_id,
            "message": "帮我查订单ORD-20260502-002"
        })
        print("Chat send:", r.json()["code"])

        r = await c.get(f"{BASE_URL}/api/panel/{session_id}")
        panel = r.json()
        print("Panel code:", panel["code"])
        profile = panel["data"]["user_profile"]
        print(f"用户画像槽位总数: {len(profile)}")
        realtime = [k for k in profile if k in REALTIME_SLOTS]
        preset = [k for k in profile if k not in REALTIME_SLOTS]
        print(f"实时抽取槽位: {len(realtime)}")
        print(f"低频预设槽位: {len(preset)}")
        print(f"实时槽位列表: {realtime}")
        print(f"预设槽位列表: {preset}")


asyncio.run(test())
