"""
调试与性能分析示例：
- logging 基础用法
- timeit 微基准
- cProfile + pstats 统计热点
"""

from __future__ import annotations

import cProfile
import logging
import pstats
import random
import timeit
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("debug_profile_demo")


def heavy_compute(n: int) -> int:
    """模拟耗时计算：排序 + 求和"""
    data = [random.randint(1, 1000) for _ in range(n)]
    data.sort()
    return sum(data)


def light_compute(n: int) -> int:
    """较轻的计算：直接使用公式求和"""
    return n * (n + 1) // 2


def run_timeit():
    """对比微基准"""
    t_heavy = timeit.timeit("heavy_compute(2000)", number=20, globals=globals())
    t_light = timeit.timeit("light_compute(2000)", number=200, globals=globals())
    logger.info("heavy_compute 耗时：%.4fs /20 次", t_heavy)
    logger.info("light_compute 耗时：%.4fs /200 次", t_light)


def run_cprofile():
    """分析 heavy_compute 性能热点"""
    profile = cProfile.Profile()
    profile.enable()
    heavy_compute(5000)
    profile.disable()

    stats = pstats.Stats(profile).strip_dirs().sort_stats("cumulative")
    logger.info("cProfile Top 8（按累计耗时）")
    stats.print_stats(8)


if __name__ == "__main__":
    logger.info("演示开始")
    run_timeit()
    run_cprofile()
    logger.info("演示结束")
