#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步编程练习
练习：async/await、gather、并发限制、在线程池中运行同步代码
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Iterable, List


print("=== 练习1：并发获取用户信息 ===")
"""
题目：实现 async fetch_user(user_id) 和 async fetch_many_users(ids)
要求：
1. fetch_user(user_id) 模拟网络请求（asyncio.sleep），返回 dict：
   {"id": user_id, "name": f"用户{user_id}"}
2. fetch_many_users(ids) 使用 asyncio.gather 并发获取多个用户
3. 在 main 中运行并打印结果
"""


async def fetch_user(user_id: int) -> dict:
    """模拟异步获取用户信息。"""
    # TODO: 在这里实现
    raise NotImplementedError


async def fetch_many_users(ids: Iterable[int]) -> list[dict]:
    """并发获取多个用户信息。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n=== 练习2：使用信号量限制并发 ===")
"""
题目：实现 limited_fetch(urls, limit)
要求：
1. 假设有一个 async fake_request(url) 函数（你可以自己实现）
2. 使用 asyncio.Semaphore 限制同时进行的请求数量
3. 返回所有请求结果列表
"""


async def limited_fetch(urls: list[str], limit: int = 3) -> list[dict]:
    """使用信号量限制并发请求数量。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n=== 练习3：在线程池中运行同步阻塞代码 ===")
"""
题目：实现 async run_blocking_in_executor(func, *args, **kwargs)
要求：
1. 在异步函数中，将同步阻塞函数放入线程池执行
2. 返回函数的返回值
3. 可参考 demo_async_programming.py 中 integrate_sync_code 的写法
"""


async def run_blocking_in_executor(func, *args, **kwargs):
    """在异步上下文中运行同步阻塞函数。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n异步编程练习：建议在命令行中使用 asyncio.run 运行你编写的顶层协程进行测试。")

