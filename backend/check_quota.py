import asyncio
from api.kimi_client import kimi_client

async def main():
    print("正在查询Kimi API配额信息...\n")
    
    # 查询API配额
    result = await kimi_client.get_api_quota()
    
    if result["success"]:
        print("📊 API配额信息:")
        print(f"   限流限制: {result['rate_limit']}")
        print(f"   剩余配额: {result['rate_remaining']}")
        print("\n📦 可用模型:")
        for model in result.get("model_info", []):
            print(f"   - {model.get('id', '未知')}")
    else:
        print(f"❌ 查询失败: {result['message']}")
        if "detail" in result:
            print(f"   详情: {result['detail']}")
    
    # 打印当前配置
    print("\n⚙️ 当前配置:")
    print(f"   API Key: {kimi_client.api_key[:10]}...")
    print(f"   模型: {kimi_client.model}")
    print(f"   应用限流: 每分钟{10}次请求")

if __name__ == "__main__":
    asyncio.run(main())