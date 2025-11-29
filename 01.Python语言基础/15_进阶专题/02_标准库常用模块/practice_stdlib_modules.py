#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准库常用模块练习
练习：datetime / collections / itertools / functools
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import reduce
from itertools import chain, groupby
from typing import Iterable, List


print("=== 练习1：datetime - 日期区间 ===")
"""
题目：实现一个函数，给定起始日期字符串，返回连续 7 天的日期列表。
要求：
1. 输入格式为 'YYYY-MM-DD'，例如 '2024-01-01'
2. 返回列表中的每个元素也是 'YYYY-MM-DD' 形式的字符串
3. 使用 datetime 和 timedelta 进行日期加减
"""


def week_dates(start_date_str: str) -> list[str]:
    """返回从给定日期开始的连续 7 天日期字符串。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(week_dates("2024-01-01"))


print("\n=== 练习2：collections - 计数与分组 ===")
"""
题目：使用 Counter 和 defaultdict 完成单词统计与分组。
要求：
1. 给定一段文本，按空格切分为单词（忽略大小写）
2. 使用 Counter 统计每个单词出现次数
3. 使用 defaultdict(list) 按单词长度分组，得到：长度 -> [单词列表]
"""


def analyze_words(text: str) -> tuple[Counter, dict[int, list[str]]]:
    """统计单词频率并按长度分组。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# text = "Python is great and python is simple but powerful"
# counter, groups = analyze_words(text)
# print("词频：", counter)
# print("按长度分组：", groups)


print("\n=== 练习3：itertools - 链接与分组 ===")
"""
题目：
1. 使用 chain 将多个列表链接为一个迭代器
2. 使用 groupby 对已排序的列表按某个键分组

示例数据：
    users = [
        {"name": "A", "dept": "技术"},
        {"name": "B", "dept": "技术"},
        {"name": "C", "dept": "销售"},
        {"name": "D", "dept": "销售"},
    ]
"""


def merge_lists(*lists: Iterable[int]) -> list[int]:
    """使用 chain 合并多个整数列表。"""
    # TODO: 在这里实现
    raise NotImplementedError


def group_users_by_dept(users: list[dict]) -> dict[str, list[dict]]:
    """使用 groupby 按部门分组用户（注意需要先排序）。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(merge_lists([1, 2], [3, 4], [5]))
# users = [
#     {"name": "A", "dept": "技术"},
#     {"name": "B", "dept": "技术"},
#     {"name": "C", "dept": "销售"},
#     {"name": "D", "dept": "销售"},
# ]
# print(group_users_by_dept(users))


print("\n=== 练习4：functools - 归约与数据类 ===")
"""
题目：
1. 使用 reduce 实现一个简单的累乘函数 product(numbers)
2. 使用 dataclass 定义一个简单的订单 Order，包含字段：
   - id: int
   - price: float
   - quantity: int
3. 编写函数 total_amount(orders) 计算订单总金额
"""


def product(numbers: Iterable[int]) -> int:
    """使用 reduce 计算所有数字的乘积。"""
    # TODO: 在这里实现
    raise NotImplementedError


@dataclass
class Order:
    """订单数据类"""

    id: int
    price: float
    quantity: int


def total_amount(orders: Iterable[Order]) -> float:
    """计算所有订单的总金额。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(product([2, 3, 4]))
# orders = [
#     Order(id=1, price=10.0, quantity=2),
#     Order(id=2, price=20.0, quantity=1),
# ]
# print(total_amount(orders))


print("\n标准库常用模块练习：建议完成所有 TODO，并在 REPL 中多次尝试不同输入。")

