#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步编程入门示例
演示：asyncio、async/await、协程、并发执行
Python 3.10+
"""

import asyncio
import time
from typing import List

# ========== 1. 基础概念 ==========
print("=== 异步编程基础 ===")

# 1.1 同步 vs 异步对比
def sync_task(name, delay):
    """同步任务"""
    print(f"[同步] {name} 开始")
    time.sleep(delay)
    print(f"[同步] {name} 完成")
    return f"{name}的结果"

async def async_task(name, delay):
    """异步任务"""
    print(f"[异步] {name} 开始")
    await asyncio.sleep(delay)  # 异步睡眠
    print(f"[异步] {name} 完成")
    return f"{name}的结果"

# 同步执行（串行）
print("\n--- 同步执行 ---")
start = time.time()
result1 = sync_task("任务1", 1)
result2 = sync_task("任务2", 1)
result3 = sync_task("任务3", 1)
print(f"总耗时：{time.time() - start:.2f}秒\n")


# 异步执行（并发）
async def run_async_tasks():
    print("--- 异步执行 ---")
    start = time.time()
    results = await asyncio.gather(
        async_task("任务1", 1),
        async_task("任务2", 1),
        async_task("任务3", 1)
    )
    print(f"总耗时：{time.time() - start:.2f}秒")
    print(f"结果：{results}\n")

# 运行异步函数
asyncio.run(run_async_tasks())


# ========== 2. async/await 语法 ==========
print("=== async/await 语法 ===")

async def fetch_data(user_id: int) -> dict:
    """模拟异步获取数据"""
    print(f"正在获取用户{user_id}的数据...")
    await asyncio.sleep(0.5)  # 模拟网络延迟
    return {"id": user_id, "name": f"用户{user_id}"}

async def process_data(data: dict) -> dict:
    """模拟异步处理数据"""
    print(f"正在处理用户{data['id']}的数据...")
    await asyncio.sleep(0.3)
    return {**data, "processed": True}

async def main_workflow():
    """主工作流"""
    print("\n--- 顺序执行 ---")
    # 顺序执行
    user_data = await fetch_data(1)
    processed_data = await process_data(user_data)
    print(f"结果：{processed_data}\n")

    print("--- 并发执行多个用户 ---")
    # 并发获取多个用户数据
    users = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(f"获取到{len(users)}个用户")

asyncio.run(main_workflow())


# ========== 3. 任务管理 ==========
print("\n=== 任务管理 ===")

async def countdown(name: str, seconds: int):
    """倒计时任务"""
    for i in range(seconds, 0, -1):
        print(f"{name}: {i}秒")
        await asyncio.sleep(1)
    print(f"{name}: 完成！")

async def task_management():
    print("--- 创建和管理任务 ---")

    # 创建任务
    task1 = asyncio.create_task(countdown("任务1", 3))
    task2 = asyncio.create_task(countdown("任务2", 2))

    # 等待所有任务完成
    await task1
    await task2
    print("所有任务完成\n")

    # 带超时的任务
    print("--- 超时控制 ---")
    try:
        await asyncio.wait_for(countdown("长任务", 5), timeout=2)
    except asyncio.TimeoutError:
        print("任务超时！\n")

asyncio.run(task_management())


# ========== 4. 异步迭代器和生成器 ==========
print("=== 异步迭代器 ===")

async def async_range(start, end):
    """异步生成器"""
    for i in range(start, end):
        await asyncio.sleep(0.1)
        yield i

async def async_iteration():
    print("--- 异步for循环 ---")
    async for num in async_range(1, 6):
        print(f"生成数字：{num}")

asyncio.run(async_iteration())


# ========== 5. 异步上下文管理器 ==========
print("\n=== 异步上下文管理器 ===")

class AsyncDatabaseConnection:
    """模拟异步数据库连接"""

    async def __aenter__(self):
        print("连接数据库...")
        await asyncio.sleep(0.2)
        print("数据库已连接")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("关闭数据库连接...")
        await asyncio.sleep(0.1)
        print("数据库已关闭")

    async def query(self, sql: str):
        """执行查询"""
        print(f"执行SQL：{sql}")
        await asyncio.sleep(0.3)
        return [{"id": 1, "name": "数据"}]

async def database_operation():
    async with AsyncDatabaseConnection() as db:
        result = await db.query("SELECT * FROM users")
        print(f"查询结果：{result}")

asyncio.run(database_operation())


# ========== 6. 并发模式 ==========
print("\n=== 并发模式 ===")

async def http_request(url: str) -> dict:
    """模拟HTTP请求"""
    print(f"请求：{url}")
    await asyncio.sleep(0.5)
    return {"url": url, "status": 200}

async def concurrent_requests():
    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
        "https://api.example.com/users/4",
    ]

    print("--- 方法1：gather（全部成功或失败）---")
    start = time.time()
    results = await asyncio.gather(*[http_request(url) for url in urls])
    print(f"耗时：{time.time() - start:.2f}秒")
    print(f"成功请求：{len(results)}个\n")

    print("--- 方法2：as_completed（按完成顺序）---")
    start = time.time()
    tasks = [asyncio.create_task(http_request(url)) for url in urls]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  完成：{result['url']}")
    print(f"耗时：{time.time() - start:.2f}秒\n")

asyncio.run(concurrent_requests())


# ========== 7. 信号量（并发限制）==========
print("=== 并发限制 ===")

async def limited_request(sem: asyncio.Semaphore, url: str):
    """限制并发的请求"""
    async with sem:  # 获取信号量
        print(f"开始请求：{url}")
        await asyncio.sleep(1)
        print(f"完成请求：{url}")
        return {"url": url}

async def rate_limiting():
    # 最多同时3个请求
    sem = asyncio.Semaphore(3)

    urls = [f"https://api.example.com/{i}" for i in range(10)]

    print(f"--- 限制并发数为3 ---")
    start = time.time()
    results = await asyncio.gather(
        *[limited_request(sem, url) for url in urls]
    )
    print(f"完成10个请求，耗时：{time.time() - start:.2f}秒\n")

asyncio.run(rate_limiting())


# ========== 8. 异步队列 ==========
print("=== 异步队列 ===")

async def producer(queue: asyncio.Queue, n: int):
    """生产者"""
    for i in range(n):
        item = f"item-{i}"
        await queue.put(item)
        print(f"生产：{item}")
        await asyncio.sleep(0.1)

async def consumer(queue: asyncio.Queue, name: str):
    """消费者"""
    while True:
        item = await queue.get()
        print(f"消费者{name}处理：{item}")
        await asyncio.sleep(0.3)
        queue.task_done()

async def producer_consumer():
    queue = asyncio.Queue(maxsize=5)

    # 创建1个生产者和2个消费者
    producer_task = asyncio.create_task(producer(queue, 10))

    consumers = [
        asyncio.create_task(consumer(queue, "A")),
        asyncio.create_task(consumer(queue, "B")),
    ]

    # 等待生产者完成
    await producer_task

    # 等待队列被处理完
    await queue.join()

    # 取消消费者
    for c in consumers:
        c.cancel()

asyncio.run(producer_consumer())


# ========== 9. 实战示例：批量下载 ==========
print("\n=== 实战：模拟批量下载 ===")

async def download_file(url: str, filename: str) -> dict:
    """模拟文件下载"""
    print(f"开始下载：{filename}")
    # 模拟不同大小的文件（不同下载时间）
    import random
    download_time = random.uniform(0.5, 2.0)
    await asyncio.sleep(download_time)
    print(f"完成下载：{filename}（耗时{download_time:.1f}秒）")
    return {"filename": filename, "size": int(download_time * 1024)}

async def batch_download():
    files = [
        ("https://example.com/file1.zip", "file1.zip"),
        ("https://example.com/file2.zip", "file2.zip"),
        ("https://example.com/file3.zip", "file3.zip"),
        ("https://example.com/file4.zip", "file4.zip"),
        ("https://example.com/file5.zip", "file5.zip"),
    ]

    print(f"开始批量下载{len(files)}个文件...")
    start = time.time()

    # 限制并发数为3
    sem = asyncio.Semaphore(3)

    async def download_with_limit(url, filename):
        async with sem:
            return await download_file(url, filename)

    results = await asyncio.gather(
        *[download_with_limit(url, fn) for url, fn in files]
    )

    total_size = sum(r['size'] for r in results)
    elapsed = time.time() - start

    print(f"\n下载完成：")
    print(f"  文件数：{len(results)}")
    print(f"  总大小：{total_size} KB")
    print(f"  总耗时：{elapsed:.2f}秒")

asyncio.run(batch_download())


# ========== 10. 与同步代码集成 ==========
print("\n=== 与同步代码集成 ===")

def blocking_operation():
    """阻塞的同步操作"""
    print("执行阻塞操作...")
    time.sleep(1)
    return "阻塞操作结果"

async def integrate_sync_code():
    print("--- 在异步中运行同步代码 ---")

    # 在线程池中运行阻塞操作
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_operation)
    print(f"结果：{result}")

asyncio.run(integrate_sync_code())


print("\n=== 异步编程关键点总结 ===")
print("""
1. async def 定义异步函数（协程）
2. await 等待异步操作完成
3. asyncio.run() 运行顶层异步函数
4. asyncio.gather() 并发执行多个协程
5. asyncio.create_task() 创建任务
6. async with 异步上下文管理器
7. async for 异步迭代
8. asyncio.Semaphore 限制并发数
9. asyncio.Queue 异步队列

性能提升场景：
✅ IO密集型：网络请求、文件操作、数据库查询
❌ CPU密集型：使用多进程而非异步
""")

print("\n异步编程演示完成！")
