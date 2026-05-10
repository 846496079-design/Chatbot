import requests
import json
import time
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

print("=" * 60)
print("          并行调用测试")
print("=" * 60)

# 测试分析端点
print("\n=== 测试分析端点 ===")
start = time.time()
r = requests.post(f'{BASE_URL}/api/chat/analyze', 
    json={'session_id': 'test_parallel', 'message': '我想给我老公买一份四十岁生日礼物你有什么推荐吗？'})
elapsed = (time.time() - start) * 1000
print(f"状态码: {r.status_code}, 耗时: {elapsed:.0f}ms")
data = r.json()
if data.get('code') == 0:
    d = data['data']
    print(f"意图: {d['intent']['name']} (置信度: {d['intent']['confidence']})")
    print(f"情绪: {d['emotion']['label']} (置信度: {d['emotion']['confidence']})")
    print(f"业务槽位: {d['structured_data']['business_slots']}")
    print(f"画像更新: {d['structured_data']['profile_updates']}")
    print(f"Token累计: {d['token_usage']}")
else:
    print(f"失败: {data}")

# 测试流式端点
print("\n=== 测试流式端点 ===")
start = time.time()
r = requests.post(f'{BASE_URL}/api/chat/quick/stream',
    json={'session_id': 'test_parallel2', 'message': '你好'}, stream=True)
first_char_time = None
full_content = ""
for chunk in r.iter_content(chunk_size=1024):
    if chunk:
        if first_char_time is None:
            first_char_time = (time.time() - start) * 1000
        text = chunk.decode('utf-8')
        if 'data: ' in text:
            try:
                for line in text.split('\n'):
                    if line.startswith('data: '):
                        j = json.loads(line[6:])
                        if j.get('type') == 'text':
                            full_content += j.get('content', '')
                        elif j.get('type') == 'done':
                            print(f"首字延迟: {first_char_time:.0f}ms")
                            print(f"完整回复: {full_content}")
                            print(f"Token累计: {j.get('token_usage', {})}")
            except:
                pass

total_elapsed = (time.time() - start) * 1000
print(f"总耗时: {total_elapsed:.0f}ms")
print("\n测试完成")