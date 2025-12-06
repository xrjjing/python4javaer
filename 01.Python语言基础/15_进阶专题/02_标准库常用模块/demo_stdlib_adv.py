"""标准库进阶示例：contextlib / itertools 新增工具 / hashlib-hmac / base64 / cached_property"""

from __future__ import annotations

import base64
import hashlib
import hmac
from contextlib import contextmanager, suppress
from functools import cached_property, lru_cache, partial
from itertools import batched, pairwise
from typing import Iterator, List


def demo_hashlib_hmac() -> None:
    msg = b"hello"
    digest = hashlib.sha256(msg).hexdigest()
    mac = hmac.new(b"secret", msg, hashlib.sha256).hexdigest()
    print("sha256:", digest)
    print("hmac:", mac)


def demo_base64() -> None:
    encoded = base64.b64encode(b"hello world")
    decoded = base64.b64decode(encoded)
    print("base64:", encoded, "decoded:", decoded)


@contextmanager
def open_upper(path: str):
    f = open(path, "r", encoding="utf-8")
    try:
        yield (line.upper() for line in f)
    finally:
        f.close()


class Circle:
    def __init__(self, r: float):
        self.r = r

    @cached_property
    def area(self) -> float:
        print("计算 area 一次")
        return 3.14159 * self.r * self.r


def demo_itertools_new():
    print("pairwise:", list(pairwise([10, 12, 15])))
    print("batched:", list(batched(range(10), 3)))


def demo_partial_cache():
    def fetch(url: str, timeout: float = 3.0) -> str:
        return f"fetch {url} with timeout={timeout}"

    cached_fetch = lru_cache(maxsize=8)(partial(fetch, timeout=5.0))
    print(cached_fetch("https://example.com"))
    print(cached_fetch.cache_info())


def main():
    demo_hashlib_hmac()
    demo_base64()
    demo_itertools_new()
    demo_partial_cache()

    c = Circle(3)
    print("area1:", c.area)
    print("area2 (cached):", c.area)

    with suppress(FileNotFoundError):
        with open_upper("README.md") as lines:
            first_three = [next(lines) for _ in range(3)]
            print("README 前三行大写:", first_three)


if __name__ == "__main__":
    main()
