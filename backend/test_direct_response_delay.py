import asyncio
import time
import json
from api.kimi_client import kimi_client

async def test_direct_response_delay():
    """测试直接响应模式的首字延迟"""
    print("📡 测试直接响应模式（跳过意图识别）...")
    print("问题: 我想给我老公买一份四十岁生日礼物你有什么推荐吗？")
    
    user_input = "我想给我老公买一份四十岁生日礼物你有什么推荐吗？"
    
    # 记录发送请求的时间
    send_time = time.time()
    first_char_received = False
    first_char_time = 0
    total_chars = 0
    response_content = ""
    
    print("\n⏳ 发送请求...")
    
    # 使用直接响应的流式模式
    async for chunk in kimi_client.direct_response_stream(user_input, context=""):
        if chunk.strip() and not first_char_received:
            # 记录收到第一个字符的时间
            first_char_time = time.time()
            first_char_received = True
            first_char_delay = (first_char_time - send_time) * 1000  # 转换为毫秒
            
            print(f"\n✅ 首字到达！")
            print(f"   首字延迟: {first_char_delay:.2f} 毫秒")
            
        # 解析流式响应
        if chunk.strip():
            try:
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
    print(f"   {response_content[:150]}...")
    
    return {
        "first_char_delay_ms": first_char_delay,
        "total_time_ms": total_time,
        "chars": total_chars
    }

async def test_original_flow_delay():
    """测试原始流程（两次LLM调用）的首字延迟"""
    print("\n\n📡 测试原始流程（意图识别 + 响应生成）...")
    print("问题: 我想给我老公买一份四十岁生日礼物你有什么推荐吗？")
    
    from agent.graph import agent_graph
    from langchain_core.messages import HumanMessage
    
    user_input = "我想给我老公买一份四十岁生日礼物你有什么推荐吗？"
    
    send_time = time.time()
    first_char_time = 0
    
    print("\n⏳ 发送请求...")
    
    state = {
        "session_id": "test_session",
        "messages": [HumanMessage(content=user_input)],
        "current_flow": None,
        "current_intent": None,
        "current_emotion": None,
        "business_slots": {},
        "profile_slots": {},
        "negative_emotion_count": 0,
        "fallback_count": 0,
        "need_comfort": False,
        "need_escalation": False,
    }
    
    result = await agent_graph.ainvoke(state)
    
    total_time = (time.time() - send_time) * 1000
    
    reply = ""
    if result.get("messages"):
        for msg in result["messages"]:
            if hasattr(msg, "content"):
                reply = msg.content
    
    print(f"\n📊 完整响应统计:")
    print(f"   总响应时间: {total_time:.2f} 毫秒")
    print(f"   响应长度: {len(reply)} 字符")
    
    print("\n📝 响应内容预览:")
    print(f"   {reply[:150]}...")
    
    return {
        "total_time_ms": total_time,
        "chars": len(reply)
    }

async def main():
    print("=" * 60)
    print("          首字延迟优化对比测试")
    print("=" * 60)
    
    # 测试直接响应模式
    direct_result = await test_direct_response_delay()
    
    # 测试原始流程模式
    original_result = await test_original_flow_delay()
    
    print("\n\n" + "=" * 60)
    print("          测试结果对比")
    print("=" * 60)
    print(f"{'模式':<20} {'首字延迟':<15} {'总耗时':<15}")
    print("-" * 60)
    print(f"直接响应模式:  {direct_result['first_char_delay_ms']:>8.2f} ms  {direct_result['total_time_ms']:>10.2f} ms")
    print(f"原始流程模式:      N/A         {original_result['total_time_ms']:>10.2f} ms")
    print("\n💡 优化效果:")
    print(f"   - 直接响应模式首字延迟约 {direct_result['first_char_delay_ms']/1000:.1f} 秒")
    print(f"   - 原始流程模式总耗时约 {original_result['total_time_ms']/1000:.1f} 秒")
    print(f"   - 优化后首字延迟降低约 {(1 - direct_result['first_char_delay_ms']/original_result['total_time_ms'])*100:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())