#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迭代器与生成器示例
演示：可迭代对象、迭代器、生成器函数、生成器表达式
"""

# 1. 迭代器协议
print("=== 迭代器协议 ===")
class Counter:
    """计数器迭代器"""
    def __init__(self, max_value):
        self.max_value = max_value
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.max_value:
            current = self.current
            self.current += 1
            return current
        else:
            raise StopIteration

counter = Counter(5)
print("计数：")
for num in counter:
    print(num)

# 2. 使用内置迭代器函数
print("\n=== 内置迭代器函数 ===")
numbers = [1, 2, 3, 4, 5]

# iter() 获取迭代器
it = iter(numbers)
print("使用 next() 遍历：")
print(next(it))
print(next(it))
print(next(it))

# 3. 生成器函数
print("\n=== 生成器函数 ===")
def count_to(n):
    """生成1到n的数字"""
    current = 1
    while current <= n:
        yield current
        current += 1

gen = count_to(5)
print("生成器：", end="")
for num in gen:
    print(num, end=" ")
print()

# 4. 生成器的延迟计算
print("\n=== 延迟计算 ===")
def large_range():
    """大数据量生成器"""
    for i in range(1000000):
        yield i * 2

# 只生成前3个元素
gen = large_range()
print("前3个值：")
print(next(gen))
print(next(gen))
print(next(gen))

# 5. 生成器表达式
print("\n=== 生成器表达式 ===")
# 列表推导式（立即计算）
list_comp = [x**2 for x in range(10)]
print(f"列表推导式：{list_comp}")

# 生成器表达式（延迟计算）
gen_exp = (x**2 for x in range(10))
print("生成器表达式：", end="")
for num in gen_exp:
    print(num, end=" ")
print()

# 6. 使用 yield from
print("\n=== yield from ===")
def gen1():
    yield 1
    yield 2
    yield 3

def gen2():
    yield "A"
    yield from gen1()  # 委托给另一个生成器
    yield "B"

print("使用 yield from：")
for item in gen2():
    print(item)

# 7. 生成器的状态
print("\n=== 生成器状态 ===")
def simple_gen():
    print("生成器启动")
    yield 1
    print("第一次 yield 后")
    yield 2
    print("第二次 yield 后")
    yield 3
    print("生成器结束")

gen = simple_gen()
print("第一次 next：")
print(next(gen))
print("第二次 next：")
print(next(gen))
print("第三次 next：")
print(next(gen))

# 8. 无限生成器
print("\n=== 无限生成器 ===")
def infinite_counter(start=0):
    """无限计数器"""
    count = start
    while True:
        yield count
        count += 1

# 限制输出前5个
counter = infinite_counter(10)
print("从10开始的计数器（前5个）：")
for _ in range(5):
    print(next(counter))

# 9. 管道式处理
print("\n=== 管道式处理 ===")
def read_numbers():
    """读取数字"""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for num in numbers:
        yield num

def filter_even(numbers):
    """过滤偶数"""
    for num in numbers:
        if num % 2 == 0:
            yield num

def square(numbers):
    """平方"""
    for num in numbers:
        yield num ** 2

# 管道：读取 -> 过滤偶数 -> 平方
result = square(filter_even(read_numbers()))
print("管道处理结果：", list(result))

# 10. 协程概念
print("\n=== 协程示例 ===")
def coro():
    result = yield "初始值"
    print(f"收到：{result}")
    result = yield "第二个值"
    print(f"收到：{result}")

c = coro()
print("启动：", next(c))
print("发送数据：", c.send(100))
print("发送数据：", c.send(200))

# 11. itertools 模块
print("\n=== itertools 模块 ===")
from itertools import count, cycle, chain, islice

# count - 无限计数
print("计数（限制前5个）：")
for i in islice(count(1), 5):
    print(i)

# cycle - 循环
print("循环字符串：")
i = 0
for item in cycle("ABC"):
    if i >= 5:
        break
    print(item)
    i += 1

# chain - 连接多个迭代器
print("连接多个迭代器：")
for item in chain([1, 2], "ABC", [3, 4]):
    print(item)

# 12. 生成器在数据分析中的应用
print("\n=== 文件逐行处理 ===")
import os

def process_large_file(filename):
    """逐行处理大文件"""
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # 去除换行符
            line = line.strip()
            if line and not line.startswith("#"):
                yield line

# 创建测试文件
test_file = "test_large.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write("# 这是注释\n")
    f.write("有效数据1\n")
    f.write("# 另一条注释\n")
    f.write("有效数据2\n")
    f.write("有效数据3\n")

try:
    print("文件内容（跳过注释和空行）：")
    for line in process_large_file(test_file):
        print(f"  {line}")
finally:
    os.remove(test_file)
