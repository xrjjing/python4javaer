"""并发进阶示例：threading.local + multiprocessing.Pool"""

from __future__ import annotations

import threading
from multiprocessing import Pool
from typing import List


def _square(n: int) -> int:
    return n * n


def demo_process_pool() -> List[int]:
    with Pool(processes=2) as pool:
        results = pool.map(_square, [1, 2, 3, 4])
    return results


def demo_thread_local() -> None:
    local_ctx = threading.local()

    def worker(name: str) -> None:
        local_ctx.user = name
        print(threading.current_thread().name, "->", local_ctx.user)

    threads = [threading.Thread(target=worker, args=(f"user{i}",)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    print("线程本地存储演示：")
    demo_thread_local()

    print("\n进程池演示：")
    print(demo_process_pool())
