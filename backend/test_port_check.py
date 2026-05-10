import requests
import json
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

print("=== 测试8000端口服务 ===")

# 创建会话
print("\n1. 创建会话:")
r = requests.post(f"{BASE_URL}/api/session/create")
print(f"状态码: {r.status_code}")
print(f"响应: {r.text}")

if r.status_code == 200:
    session_id = r.json()["data"]["session_id"]
    
    # 发送消息
    print("\n2. 发送消息 '推荐一款手机':")
    data = {"session_id": session_id, "message": "推荐一款手机"}
    r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
    print(f"状态码: {r.status_code}")
    response = r.json()
    print(f"回复: {response['data']['reply']}")
    print(f"意图: {response['data']['intent']['name']} (置信度: {response['data']['intent']['confidence']})")