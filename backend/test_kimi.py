import asyncio
from api.kimi_client import kimi_client


async def test_kimi():
    print("=== 测试Kimi API客户端 ===")
    
    # 测试基本聊天
    print("\n1. 测试基本聊天功能:")
    messages = [{"role": "user", "content": "你好，请问你是谁？"}]
    result = await kimi_client.chat(messages)
    print(f"成功: {result.get('success')}")
    print(f"错误: {result.get('error')}")
    print(f"内容: {result.get('content')[:100] if result.get('content') else '无'}")
    
    # 测试意图分类
    print("\n2. 测试意图分类:")
    result = await kimi_client.classify_intent("我要退货", "（新会话，无历史对话）")
    print(f"成功: {result.get('success')}")
    print(f"错误: {result.get('error')}")
    print(f"意图: {result.get('intent')}")
    print(f"置信度: {result.get('confidence')}")
    print(f"情绪: {result.get('emotion')}")


asyncio.run(test_kimi())