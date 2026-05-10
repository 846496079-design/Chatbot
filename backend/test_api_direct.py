import requests
import json
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

# 创建会话
print("=== 创建会话 ===")
r = requests.post(f"{BASE_URL}/api/session/create")
print(f"状态码: {r.status_code}")
print(f"响应: {r.text}")

if r.status_code == 200:
    session_id = r.json()["data"]["session_id"]
    
    # 发送消息
    print("\n=== 发送消息 ===")
    data = {
        "session_id": session_id,
        "message": "我要退货"
    }
    r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
    print(f"状态码: {r.status_code}")
    print(f"响应: {r.text}")