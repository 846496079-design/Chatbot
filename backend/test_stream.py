import asyncio
from api.kimi_client import kimi_client

async def test_stream():
    print("测试流式响应...")
    async for chunk in kimi_client.chat_stream([{'role':'user','content':'你好'}]):
        print(f"Chunk: {chunk[:100]}")

if __name__ == "__main__":
    asyncio.run(test_stream())