"""
多线程与多进程示例

本模块演示：
1. 使用 ThreadPoolExecutor 并发请求多个 URL（IO 密集）；
2. 使用 ProcessPoolExecutor 处理 CPU 密集型计算；
3. 简单对比单线程与并发版本的写法差异。

说明：
- 这里的示例以「结构清晰」为主，没有刻意做极致性能优化；
- 在真实项目中，请结合 logging、重试策略等进行完善。
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import perf_counter
from typing import List, Tuple

import requests


def fetch_status(url: str, timeout: float = 5.0) -> tuple[str, int | None]:
    """
    请求 URL 并返回 (url, 状态码)。

    出错时返回 (url, None)。
    """
    try:
        resp = requests.get(url, timeout=timeout)
        return url, resp.status_code
    except requests.RequestException:
        return url, None


def fetch_all_status_sequential(urls: list[str]) -> list[tuple[str, int | None]]:
    """
    单线程版本：顺序请求一组 URL。
    """
    return [fetch_status(url) for url in urls]


def fetch_all_status_threaded(
    urls: list[str],
    max_workers: int = 5,
) -> list[tuple[str, int | None]]:
    """
    使用线程池并发请求一组 URL。
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_status, url) for url in urls]
        return [f.result() for f in futures]


def count_primes(n: int) -> int:
    """
    粗略统计 [2, n) 范围内的素数个数。

    注意：这里使用的是非常朴素的算法，仅用于演示 CPU 密集任务。
    """
    if n <= 2:
        return 0

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True

    return sum(1 for i in range(2, n) if is_prime(i))


def count_primes_sequential(bounds: list[int]) -> list[int]:
    """
    单进程版本：依次计算多个上界的素数数量。
    """
    return [count_primes(b) for b in bounds]


def count_primes_parallel(
    bounds: list[int],
    max_workers: int = 4,
) -> list[int]:
    """
    使用进程池并行计算多个上界的素数数量。

    注意：在 Windows 上调用本函数时，需要保证在

        if __name__ == "__main__":
            ...

    保护下运行。
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(count_primes, b) for b in bounds]
        return [f.result() for f in futures]


def benchmark_http(urls: list[str]) -> None:
    """
    对比单线程与多线程请求 URL 的耗时（简单基准）。
    """
    print("=== HTTP 请求基准测试 ===")

    start = perf_counter()
    seq_result = fetch_all_status_sequential(urls)
    t_seq = perf_counter() - start

    start = perf_counter()
    thr_result = fetch_all_status_threaded(urls)
    t_thr = perf_counter() - start

    print(f"单线程结果: {seq_result}")
    print(f"线程池结果: {thr_result}")
    print(f"单线程耗时: {t_seq:.3f}s, 线程池耗时: {t_thr:.3f}s")


def benchmark_primes(bounds: list[int]) -> None:
    """
    对比单进程与多进程计算素数数量的耗时。
    """
    print("=== 素数计算基准测试 ===")

    start = perf_counter()
    seq_result = count_primes_sequential(bounds)
    t_seq = perf_counter() - start

    start = perf_counter()
    par_result = count_primes_parallel(bounds)
    t_par = perf_counter() - start

    print(f"单进程结果: {seq_result}")
    print(f"多进程结果: {par_result}")
    print(f"单进程耗时: {t_seq:.3f}s, 多进程耗时: {t_par:.3f}s")


def _demo() -> None:
    """
    简单演示入口。

    推荐在命令行中运行本文件，观察输出：

    python 01.Python语言基础/15_进阶专题/06_多线程与多进程/demo_concurrency.py
    """
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]
    benchmark_http(urls)

    bounds = [50_000, 60_000, 70_000, 80_000]
    benchmark_primes(bounds)


if __name__ == "__main__":
    _demo()

