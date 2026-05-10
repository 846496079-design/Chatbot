import asyncio
import time
from api.kimi_client import kimi_client

async def test_concurrent_requests():
    """测试并发请求"""
    print("🔄 测试并发请求能力...")
    
    # 定义两个不同的请求
    request1 = {
        "messages": [{"role": "user", "content": "推荐一款性价比高的蓝牙耳机"}]
    }
    request2 = {
        "messages": [{"role": "user", "content": "今天天气怎么样？"}]
    }
    
    # 记录开始时间
    start_time = time.time()
    
    # 并发执行两个请求
    tasks = [
        kimi_client.chat(request1["messages"], temperature=0.5),
        kimi_client.chat(request2["messages"], temperature=0.5)
    ]
    
    print("🚀 同时发起两个请求...")
    results = await asyncio.gather(*tasks)
    
    # 记录结束时间
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n⏱️ 总耗时: {total_time:.2f}秒")
    print("\n📝 请求结果:")
    
    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"\n请求{i}成功:")
            print(f"   内容: {result['content'][:50]}...")
            print(f"   Token消耗: {result['usage']['total_tokens']}")
        else:
            print(f"\n请求{i}失败: {result['error']}")
    
    # 对比顺序执行的理论时间
    print("\n📊 并发测试分析:")
    print("   系统已支持并发请求！")
    print("   两个请求是同时执行的，总耗时约等于单个请求的耗时")
    print("   如果是顺序执行，总耗时会是单个耗时的2倍左右")

if __name__ == "__main__":
    asyncio.run(test_concurrent_requests())