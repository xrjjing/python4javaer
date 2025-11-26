#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迭代器与生成器练习题
练习：迭代器协议、生成器函数、生成器表达式、itertools
"""

# ========== 练习1：实现迭代器 ==========
print("=== 练习1：范围迭代器 ===")
"""
题目：创建一个范围迭代器类 MyRange，模仿内置的 range()
要求：
1. 实现 __init__(self, start, end, step=1) 初始化
2. 实现 __iter__(self) 返回迭代器自身
3. 实现 __next__(self) 返回下一个值
4. 当达到 end 时抛出 StopIteration
5. 支持正向和反向迭代（step可以为负数）
"""


class MyRange:
    """自定义范围迭代器"""

    def __init__(self, start, end, step=1):
        """
        初始化范围

        Args:
            start: 起始值
            end: 结束值（不包含）
            step: 步长
        """
        # TODO: 在这里实现你的代码
        pass

    def __iter__(self):
        """返回迭代器自身"""
        # TODO: 在这里实现你的代码
        pass

    def __next__(self):
        """
        返回下一个值

        Returns:
            int: 下一个值

        Raises:
            StopIteration: 迭代结束
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码
print("正向迭代：")
for i in MyRange(0, 5):
    print(i, end=" ")
print()

print("带步长的迭代：")
for i in MyRange(0, 10, 2):
    print(i, end=" ")
print()

print("反向迭代：")
for i in MyRange(10, 0, -2):
    print(i, end=" ")
print()


# ========== 练习2：生成器函数 ==========
print("\n=== 练习2：斐波那契数列生成器 ===")
"""
题目：编写生成器函数 fibonacci(n)，生成前n个斐波那契数
要求：
1. 使用 yield 关键字
2. 斐波那契数列：0, 1, 1, 2, 3, 5, 8, 13, ...
3. 每次调用生成一个数
4. 生成n个数后停止
"""


def fibonacci(n):
    """
    斐波那契数列生成器

    Args:
        n: 生成的数量

    Yields:
        int: 斐波那契数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
print("前10个斐波那契数：")
for num in fibonacci(10):
    print(num, end=" ")
print()


# ========== 练习3：生成器表达式 ==========
print("\n=== 练习3：数据过滤和转换 ===")
"""
题目：使用生成器表达式完成以下任务
要求：
1. 创建生成器 even_squares，生成 1-20 中偶数的平方
2. 创建生成器 filtered_words，从单词列表中筛选长度大于5的单词
3. 使用生成器表达式，不要使用列表推导式
"""

# TODO: 在这里实现你的代码
# even_squares = ...
# filtered_words = ...

# 测试代码（取消注释）
# print("偶数的平方：")
# for num in even_squares:
#     print(num, end=" ")
# print()
#
# words = ["apple", "banana", "cat", "dog", "elephant", "tiger"]
# print("\n长度大于5的单词：")
# for word in filtered_words:
#     print(word)


# ========== 练习4：yield from 委托 ==========
print("\n=== 练习4：嵌套数据展平 ===")
"""
题目：编写生成器函数 flatten(nested_list)，展平嵌套列表
要求：
1. 使用 yield from 委托给子生成器
2. 支持任意层级的嵌套
3. 例如：[[1, 2], [3, 4, 5]] -> 1, 2, 3, 4, 5
"""


def flatten(nested_list):
    """
    展平嵌套列表

    Args:
        nested_list: 嵌套列表

    Yields:
        元素
    """
    # TODO: 在这里实现你的代码
    # 提示：检查元素是否是列表，如果是则递归调用flatten
    pass


# 测试代码
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
print("展平嵌套列表：")
print(list(flatten(nested)))

nested2 = [[1, [2, 3]], [4, [5, [6, 7]]]]
print("展平深层嵌套：")
print(list(flatten(nested2)))


# ========== 练习5：无限生成器 ==========
print("\n=== 练习5：质数生成器 ===")
"""
题目：创建无限质数生成器 primes()
要求：
1. 使用 while True 创建无限循环
2. 逐个生成质数：2, 3, 5, 7, 11, 13, ...
3. 使用 yield 返回每个质数
4. 实现辅助函数 is_prime(n) 判断是否是质数
"""


def is_prime(n):
    """
    判断是否是质数

    Args:
        n: 待判断的数

    Returns:
        bool: 是否是质数
    """
    # TODO: 在这里实现你的代码
    pass


def primes():
    """
    无限质数生成器

    Yields:
        int: 质数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（生成前15个质数）
print("前15个质数：")
prime_gen = primes()
for _ in range(15):
    print(next(prime_gen), end=" ")
print()


# ========== 练习6：管道式处理 ==========
print("\n=== 练习6：数据处理管道 ===")
"""
题目：创建数据处理管道，处理数字序列
要求：
1. 生成器 read_numbers(data)：读取数字列表
2. 生成器 filter_positive(numbers)：过滤正数
3. 生成器 square(numbers)：计算平方
4. 生成器 limit(numbers, n)：限制输出前n个
5. 组合这些生成器形成处理管道
"""


def read_numbers(data):
    """
    读取数字

    Args:
        data: 数字列表

    Yields:
        int: 数字
    """
    # TODO: 在这里实现你的代码
    pass


def filter_positive(numbers):
    """
    过滤正数

    Args:
        numbers: 数字生成器

    Yields:
        int: 正数
    """
    # TODO: 在这里实现你的代码
    pass


def square(numbers):
    """
    计算平方

    Args:
        numbers: 数字生成器

    Yields:
        int: 平方值
    """
    # TODO: 在这里实现你的代码
    pass


def limit(numbers, n):
    """
    限制输出数量

    Args:
        numbers: 数字生成器
        n: 数量限制

    Yields:
        int: 数字（最多n个）
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
data = [-5, 3, -2, 8, 0, -1, 4, 6, -3, 7, 2]
print(f"原始数据：{data}")

# 管道：读取 -> 过滤正数 -> 平方 -> 限制前5个
pipeline = limit(square(filter_positive(read_numbers(data))), 5)
result = list(pipeline)
print(f"处理结果：{result}")


# ========== 练习7：itertools 应用 ==========
print("\n=== 练习7：itertools 工具 ===")
"""
题目：使用 itertools 模块完成以下任务
要求：
1. 使用 count() 和 islice() 生成前10个从5开始的奇数
2. 使用 cycle() 和 islice() 循环打印 "ABC" 10次
3. 使用 chain() 连接三个列表
4. 使用 combinations() 生成 [1,2,3,4] 的所有2元组合
"""

from itertools import count, islice, cycle, chain, combinations

# TODO: 任务1 - 生成奇数
print("前10个奇数（从5开始）：")
# odd_numbers = ...
# for num in odd_numbers:
#     print(num, end=" ")
# print()

# TODO: 任务2 - 循环字符
print("\n循环打印ABC（10次）：")
# letters = ...
# for char in letters:
#     print(char, end="")
# print()

# TODO: 任务3 - 连接列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]
print("\n连接列表：")
# merged = ...
# print(list(merged))

# TODO: 任务4 - 生成组合
numbers = [1, 2, 3, 4]
print("\n所有2元组合：")
# combos = ...
# for combo in combos:
#     print(combo)


# ========== 练习8：综合练习 - 文件数据处理 ==========
print("\n=== 练习8：日志文件处理生成器 ===")
"""
题目：创建日志文件处理生成器
要求：
1. 生成器 read_log_lines(filename)：逐行读取日志文件
2. 生成器 parse_log_entry(lines)：解析日志条目（提取时间戳和消息）
3. 生成器 filter_errors(entries)：只保留ERROR级别的日志
4. 使用管道组合这些生成器
"""

import os


def read_log_lines(filename):
    """
    逐行读取日志文件

    Args:
        filename: 文件名

    Yields:
        str: 日志行（去除换行符和空行）
    """
    # TODO: 在这里实现你的代码
    pass


def parse_log_entry(lines):
    """
    解析日志条目

    Args:
        lines: 日志行生成器

    Yields:
        dict: 日志条目字典，包含 level 和 message
            例如：{"level": "ERROR", "message": "连接失败"}
    """
    # TODO: 在这里实现你的代码
    # 提示：日志格式为 "LEVEL: message"
    pass


def filter_errors(entries):
    """
    过滤ERROR级别日志

    Args:
        entries: 日志条目生成器

    Yields:
        dict: ERROR级别的日志条目
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
log_file = "test_app.log"

# 创建测试日志文件
log_content = """INFO: 应用启动
WARNING: 内存使用率70%
ERROR: 数据库连接失败
INFO: 重试连接
ERROR: 文件未找到
WARNING: 磁盘空间不足
ERROR: 网络超时
INFO: 数据保存成功
"""

with open(log_file, "w", encoding="utf-8") as f:
    f.write(log_content)

# 使用管道处理日志
print("ERROR级别的日志：")
errors = filter_errors(parse_log_entry(read_log_lines(log_file)))
for entry in errors:
    print(f"  {entry['level']}: {entry['message']}")

# 清理文件
if os.path.exists(log_file):
    os.remove(log_file)


print("\n迭代器与生成器练习完成！")
print("\n提示：完成所有TODO部分后，运行此文件查看结果")
