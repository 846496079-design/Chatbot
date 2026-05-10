import asyncio
import time
import json

async def test_raw_api():
    """测试直接调用Kimi API的耗时"""
    print("📡 测试直接调用Kimi API...")
    from api.kimi_client import kimi_client
    
    start = time.time()
    result = await kimi_client.chat([{'role': 'user', 'content': '你好'}])
    elapsed = (time.time() - start) * 1000
    
    print(f"   耗时: {elapsed:.2f} ms")
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"   内容: {result['content'][:50]}")
    else:
        print(f"   错误: {result.get('error')}")
    
    return {"api_time_ms": elapsed, "success": result['success']}

async def test_direct_response():
    """测试直接响应模式的耗时"""
    print("\n📡 测试直接响应模式...")
    from api.kimi_client import kimi_client
    
    start = time.time()
    result = await kimi_client.direct_response("你好", "")
    elapsed = (time.time() - start) * 1000
    
    print(f"   耗时: {elapsed:.2f} ms")
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"   内容: {result['reply'][:50]}")
    
    return {"direct_time_ms": elapsed, "success": result['success']}

async def test_classify_intent():
    """测试意图识别的耗时"""
    print("\n📡 测试意图识别...")
    from api.kimi_client import kimi_client
    
    start = time.time()
    result = await kimi_client.classify_intent("你好", "")
    elapsed = (time.time() - start) * 1000
    
    print(f"   耗时: {elapsed:.2f} ms")
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"   意图: {result.get('intent')}")
    
    return {"intent_time_ms": elapsed, "success": result['success']}

async def test_generate_response():
    """测试响应生成的耗时"""
    print("\n📡 测试响应生成...")
    from api.kimi_client import kimi_client
    
    start = time.time()
    result = await kimi_client.generate_response(
        intent="general",
        emotion="neutral",
        flow_name="general_flow",
        filled_slots={},
        missing_slots=[],
        business_data="",
        conversation_history=""
    )
    elapsed = (time.time() - start) * 1000
    
    print(f"   耗时: {elapsed:.2f} ms")
    print(f"   结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"   内容: {result['reply'][:50]}")
    
    return {"generate_time_ms": elapsed, "success": result['success']}

async def test_agent_graph():
    """测试完整Agent Graph的耗时"""
    print("\n📡 测试完整Agent Graph...")
    from agent.graph import agent_graph
    from langchain_core.messages import HumanMessage
    
    start = time.time()
    state = {
        "session_id": "test_diagnose",
        "messages": [HumanMessage(content="你好")],
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
    elapsed = (time.time() - start) * 1000
    
    print(f"   耗时: {elapsed:.2f} ms")
    
    reply = ""
    if result.get("messages"):
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content"):
                reply = msg.content
                break
    
    print(f"   回复: {reply[:50]}")
    
    return {"graph_time_ms": elapsed}

async def test_network_connectivity():
    """测试网络连通性"""
    print("\n📡 测试网络连通性...")
    import httpx
    
    urls = [
        "https://api.moonshot.cn/v1",
        "https://www.baidu.com",
        "https://www.google.com"
    ]
    
    for url in urls:
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url, follow_redirects=True)
                elapsed = (time.time() - start) * 1000
                print(f"   {url}: {response.status_code} - {elapsed:.2f} ms")
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            print(f"   {url}: 失败 - {elapsed:.2f} ms - {str(e)}")

async def main():
    print("=" * 60)
    print("          响应延迟诊断")
    print("=" * 60)
    
    # 测试网络连通性
    await test_network_connectivity()
    
    # 测试各个组件
    api_result = await test_raw_api()
    intent_result = await test_classify_intent()
    generate_result = await test_generate_response()
    direct_result = await test_direct_response()
    graph_result = await test_agent_graph()
    
    print("\n" + "=" * 60)
    print("          诊断结果汇总")
    print("=" * 60)
    print(f"{'组件':<20} {'耗时(ms)':<15} {'状态'}")
    print("-" * 60)
    print(f"原始API调用: {api_result['api_time_ms']:>10.2f} ms   {'✅ 正常' if api_result['api_time_ms'] < 10000 else '⚠️ 慢'}")
    print(f"意图识别:    {intent_result['intent_time_ms']:>10.2f} ms   {'✅ 正常' if intent_result['intent_time_ms'] < 10000 else '⚠️ 慢'}")
    print(f"响应生成:    {generate_result['generate_time_ms']:>10.2f} ms   {'✅ 正常' if generate_result['generate_time_ms'] < 10000 else '⚠️ 慢'}")
    print(f"直接响应:    {direct_result['direct_time_ms']:>10.2f} ms   {'✅ 正常' if direct_result['direct_time_ms'] < 10000 else '⚠️ 慢'}")
    print(f"完整Graph:   {graph_result['graph_time_ms']:>10.2f} ms   {'✅ 正常' if graph_result['graph_time_ms'] < 15000 else '⚠️ 慢'}")
    
    print("\n💡 分析结论:")
    if api_result['api_time_ms'] > 10000:
        print("   ⚠️ API调用延迟过高，可能是网络问题或Kimi服务繁忙")
    if graph_result['graph_time_ms'] > 2 * api_result['api_time_ms']:
        print("   ⚠️ Graph流程存在额外开销，建议使用快速响应模式")
    if direct_result['direct_time_ms'] < graph_result['graph_time_ms']:
        print("   ✅ 直接响应模式更快速，建议前端使用 /api/chat/quick 端点")

if __name__ == "__main__":
    asyncio.run(main())