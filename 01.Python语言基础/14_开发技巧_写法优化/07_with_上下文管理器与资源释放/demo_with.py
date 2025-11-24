"""with 上下文管理器示例。"""

from contextlib import contextmanager
import time


@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{name} 耗时：{end - start:.6f} 秒")


with open("demo_with.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")

with timer("计算"):
    total = sum(range(1_000_00))
    print("total:", total)


