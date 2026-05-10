import httpx
import asyncio
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")


async def test_chat():
    async with httpx.AsyncClient() as c:
        # 创建会话
        r = await c.post(f"{BASE_URL}/api/session/create")
        data = r.json()
        print("=== 创建会话 ===")
        print(f"状态码: {r.status_code}")
        print(f"响应: {data}")
        session_id = data["data"]["session_id"]

        # 测试多个消息
        test_messages = [
            "我要退货",
            "上周买的鞋子我要退货",
            "你是什么模型?"
        ]

        for msg in test_messages:
            print(f"\n=== 发送消息: {msg} ===")
            r = await c.post(f"{BASE_URL}/api/chat/send", json={
                "session_id": session_id,
                "message": msg
            })
            print(f"状态码: {r.status_code}")
            response_data = r.json()
            print(f"完整响应: {response_data}")
            if response_data.get("data"):
                print(f"回复内容: {response_data['data'].get('reply', '')}")
                print(f"识别意图: {response_data['data'].get('intent', {})}")
                print(f"情绪状态: {response_data['data'].get('emotion', {})}")


asyncio.run(test_chat())