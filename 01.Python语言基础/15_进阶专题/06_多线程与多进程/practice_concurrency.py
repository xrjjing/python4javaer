#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程与多进程练习
练习：ThreadPoolExecutor / ProcessPoolExecutor / 简单基准
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import perf_counter
from typing import Iterable, List

import requests


print("=== 练习1：线程池并发请求 ===")
"""
题目：实现 fetch_all_json(urls)
要求：
1. 使用 ThreadPoolExecutor 并发请求一组返回 JSON 的 URL
2. 单个请求函数 fetch_json(url)：
   - 成功返回解析后的 dict/list
   - 失败返回 None
3. fetch_all_json 返回列表，与 urls 位置对应
"""


def fetch_json(url: str, timeout: float = 5.0):
    """单个请求函数（可直接在这里实现，也可在 demo 中参考实现思路）。"""
    # TODO: 在这里实现
    raise NotImplementedError


def fetch_all_json(urls: list[str], max_workers: int = 5) -> list:
    """使用线程池并发获取一组 JSON 结果。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n=== 练习2：进程池加速计算 ===")
"""
题目：实现 parallel_square(numbers)
要求：
1. 定义一个纯计算函数 square(n) -> n * n
2. 使用 ProcessPoolExecutor 对一组数字并行计算平方
3. 保证返回结果顺序与输入一致
"""


def parallel_square(numbers: list[int], max_workers: int = 4) -> list[int]:
    """使用进程池并行计算平方。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n=== 练习3：简单基准对比 ===")
"""
题目：实现 benchmark_fetch(urls)
要求：
1. 顺序执行：依次请求所有 URL
2. 线程池执行：使用 fetch_all_json
3. 分别记录耗时（perf_counter），打印结果
"""


def benchmark_fetch(urls: list[str]) -> None:
    """对比顺序请求与线程池请求的耗时。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n多线程与多进程练习：完成 TODO 后，可选用 httpbin / 本地服务等安全目标进行基准测试。")

