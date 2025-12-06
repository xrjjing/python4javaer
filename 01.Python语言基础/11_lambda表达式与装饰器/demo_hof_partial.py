"""
高阶函数与 functools.partial 示例。

涵盖：
- map/filter/reduce/sorted 组合
- functools.partial 预设部分参数，得到可复用的新函数
"""

from functools import partial, reduce
from operator import mul
from typing import Iterable, List


def clean_and_square(nums: Iterable[int]) -> List[int]:
    """过滤非正数 → 平方 → 倒序排序"""
    positive = filter(lambda n: n > 0, nums)
    squared = map(lambda n: n * n, positive)
    return sorted(squared, reverse=True)


def multiply_all(nums: Iterable[int]) -> int:
    """使用 reduce 计算累乘，初始值为 1"""
    return reduce(mul, nums, 1)


def apply_discount(price: float, tax_rate: float, discount: float) -> float:
    """先加税再打折，返回两位小数"""
    return round((price * (1 + tax_rate)) * (1 - discount), 2)


# 使用 partial 预设税率与折扣，生成可复用的小函数
price_with_vat = partial(apply_discount, tax_rate=0.13)        # 固定 13% 增值税
black_friday_price = partial(price_with_vat, discount=0.20)    # 黑五再打 8 折
employee_price = partial(price_with_vat, discount=0.35)        # 员工再打 65 折


if __name__ == "__main__":
    nums = [3, -1, 0, 5, 2]
    print("原始列表：", nums)
    print("过滤平方降序：", clean_and_square(nums))  # [25, 9, 4]

    factors = [2, 3, 5]
    print("累乘结果：", multiply_all(factors))  # 2 * 3 * 5 = 30

    price = 100.0
    print("含税价（不打折）：", price_with_vat(price, discount=0.0))
    print("黑五价：", black_friday_price(price))
    print("员工价：", employee_price(price))
