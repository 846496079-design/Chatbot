import requests
import json
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

print("=== 测试1: 售后退货 ===")
r = requests.post(f"{BASE_URL}/api/session/create")
session_id = r.json()["data"]["session_id"]
print(f"会话ID: {session_id}")

data = {"session_id": session_id, "message": "我要退货"}
r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
response = r.json()
print(f"回复: {response['data']['reply']}")
print(f"意图: {response['data']['intent']['name']} (置信度: {response['data']['intent']['confidence']})")
print(f"情绪: {response['data']['emotion']['label']}")
print()

print("=== 测试2: 询问模型身份 ===")
r = requests.post(f"{BASE_URL}/api/session/create")
session_id = r.json()["data"]["session_id"]
print(f"会话ID: {session_id}")

data = {"session_id": session_id, "message": "你是什么模型?"}
r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
response = r.json()
print(f"回复: {response['data']['reply']}")
print(f"意图: {response['data']['intent']['name']} (置信度: {response['data']['intent']['confidence']})")
print()

print("=== 测试3: 查询订单 ===")
r = requests.post(f"{BASE_URL}/api/session/create")
session_id = r.json()["data"]["session_id"]
print(f"会话ID: {session_id}")

data = {"session_id": session_id, "message": "帮我查一下订单"}
r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
response = r.json()
print(f"回复: {response['data']['reply']}")
print(f"意图: {response['data']['intent']['name']} (置信度: {response['data']['intent']['confidence']})")
print()

print("=== 测试4: 售前咨询 ===")
r = requests.post(f"{BASE_URL}/api/session/create")
session_id = r.json()["data"]["session_id"]
print(f"会话ID: {session_id}")

data = {"session_id": session_id, "message": "推荐一款手机"}
r = requests.post(f"{BASE_URL}/api/chat/send", json=data)
response = r.json()
print(f"回复: {response['data']['reply']}")
print(f"意图: {response['data']['intent']['name']} (置信度: {response['data']['intent']['confidence']})")