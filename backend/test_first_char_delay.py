import asyncio
import time
from api.kimi_client import kimi_client

async def test_first_char_delay():
    """测试首字延迟 - 从发送请求到收到第一个字符的时间"""
    print("📡 测试首字延迟...")
    print("问题: 我想给我老公买一份四十岁生日礼物你有什么推荐吗？")
    
    messages = [{"role": "user", "content": "我想给我老公买一份四十岁生日礼物你有什么推荐吗？"}]
    
    # 记录发送请求的时间
    send_time = time.time()
    first_char_received = False
    first_char_time = 0
    total_chars = 0
    response_content = ""
    
    print("\n⏳ 发送请求...")
    
    # 使用流式响应
    async for chunk in kimi_client.chat_stream(messages, temperature=0.5):
        if chunk.strip() and not first_char_received:
            # 记录收到第一个字符的时间
            first_char_time = time.time()
            first_char_received = True
            first_char_delay = (first_char_time - send_time) * 1000  # 转换为毫秒
            
            print(f"\n✅ 首字到达！")
            print(f"   首字延迟: {first_char_delay:.2f} 毫秒")
            
        # 累加内容
        if chunk.strip():
            # 解析流式响应（通常是JSON格式）
            try:
                import json
                if chunk.startswith('data: '):
                    chunk = chunk[6:]
                if chunk.strip() != '[DONE]':
                    data = json.loads(chunk)
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        if 'content' in delta:
                            content = delta['content']
                            response_content += content
                            total_chars += len(content)
            except:
                pass
    
    # 计算总耗时
    total_time = (time.time() - send_time) * 1000
    
    print(f"\n📊 完整响应统计:")
    print(f"   首字延迟: {first_char_delay:.2f} 毫秒")
    print(f"   总响应时间: {total_time:.2f} 毫秒")
    print(f"   响应字符数: {total_chars}")
    print(f"   平均字符速率: {total_chars / (total_time / 1000):.1f} 字符/秒")
    
    print("\n📝 响应内容预览:")
    print(f"   {response_content[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_first_char_delay())