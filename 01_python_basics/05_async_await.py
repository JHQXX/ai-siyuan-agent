"""
05 - 异步编程 (async/await)

Java 开发者注意：
- Python 的 async/await 类似 Java 的 CompletableFuture
- 但语法更简洁，用 asyncio 库管理
- 智能体开发中会经常用到（并发调用工具、流式输出等）
"""

import asyncio
import time
from typing import List


# ---------- 同步 vs 异步 ----------
def sync_task(name: str, seconds: int):
    """同步任务 - 会阻塞"""
    print(f"[{name}] 开始执行，需要 {seconds} 秒...")
    time.sleep(seconds)  # 同步 sleep，会阻塞
    print(f"[{name}] 执行完成！")
    return f"{name} 的结果"


async def async_task(name: str, seconds: int) -> str:
    """异步任务 - 不会阻塞"""
    print(f"[{name}] 开始执行，需要 {seconds} 秒...")
    await asyncio.sleep(seconds)  # 异步 sleep，不会阻塞
    print(f"[{name}] 执行完成！")
    return f"{name} 的结果"


# ---------- 顺序执行 ----------
async def sequential_demo():
    """顺序执行异步任务 - 一个接一个"""
    print("\n顺序执行（一个接一个）:")
    start = time.time()

    result1 = await async_task("任务1", 2)
    result2 = await async_task("任务2", 1)
    result3 = await async_task("任务3", 3)

    elapsed = time.time() - start
    print(f"顺序执行总耗时: {elapsed:.2f} 秒")
    print(f"结果: {result1}, {result2}, {result3}")


# ---------- 并发执行 ----------
async def concurrent_demo():
    """并发执行异步任务 - 同时进行"""
    print("\n并发执行（同时进行）:")
    start = time.time()

    # gather 类似 Java 的 CompletableFuture.allOf()
    results = await asyncio.gather(
        async_task("任务1", 2),
        async_task("任务2", 1),
        async_task("任务3", 3)
    )

    elapsed = time.time() - start
    print(f"并发执行总耗时: {elapsed:.2f} 秒")
    print(f"结果: {results}")


# ---------- 异步列表推导 ----------
async def fetch_data(url: str) -> str:
    """模拟获取数据"""
    await asyncio.sleep(0.5)
    return f"数据来自 {url}"


async def fetch_all_data(urls: List[str]) -> List[str]:
    """并发获取多个 URL 的数据"""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)


# ---------- 主程序 ----------
async def main():
    print("=" * 50)
    print("一、同步执行（对比用）")
    print("=" * 50)
    start = time.time()
    sync_task("同步任务1", 1)
    sync_task("同步任务2", 1)
    print(f"同步总耗时: {time.time() - start:.2f} 秒")

    await sequential_demo()
    await concurrent_demo()

    print("\n" + "=" * 50)
    print("三、并发获取多个数据")
    print("=" * 50)
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/orders",
        "https://api.example.com/products"
    ]
    results = await fetch_all_data(urls)
    for r in results:
        print(f"  - {r}")

    print("\n" + "=" * 50)
    print("练习：")
    print("1. 写一个异步函数，模拟调用 3 个不同的 API")
    print("2. 比较顺序执行和并发执行的时间差异")
    print("3. 思考：智能体调用多个工具时，为什么需要异步？")
    print("=" * 50)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
