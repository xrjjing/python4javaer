#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常与文件基础练习题
练习：异常处理、文件操作、JSON/CSV处理
"""

# ========== 练习1：基本异常处理 ==========
print("=== 练习1：安全除法 ===")
"""
题目：编写一个函数 safe_divide(a, b)，实现安全的除法运算
要求：
1. 捕获 ZeroDivisionError 异常
2. 捕获 TypeError 异常（如果参数不是数字）
3. 除法成功时返回结果
4. 出现异常时返回 None 并打印错误信息
"""

def safe_divide(a, b):
    """
    安全除法函数

    Args:
        a: 被除数
        b: 除数

    Returns:
        float: 除法结果，如果出错返回None
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"10 / 'a' = {safe_divide(10, 'a')}")


# ========== 练习2：自定义异常 ==========
print("\n=== 练习2：年龄验证 ===")
"""
题目：创建自定义异常类和验证函数
要求：
1. 创建自定义异常类 InvalidAgeError
2. 编写函数 validate_age(age)，验证年龄是否合法
3. 年龄必须在 0-150 之间，否则抛出 InvalidAgeError
4. 异常信息应该明确说明问题
"""

class InvalidAgeError(Exception):
    """年龄无效异常"""
    # TODO: 实现自定义异常类
    pass


def validate_age(age):
    """
    验证年龄是否合法

    Args:
        age: 年龄

    Returns:
        int: 验证通过返回年龄

    Raises:
        InvalidAgeError: 年龄不合法时抛出
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
try:
    print(f"验证年龄 25: {validate_age(25)}")
    print(f"验证年龄 -5: {validate_age(-5)}")
except InvalidAgeError as e:
    print(f"捕获异常：{e}")

try:
    print(f"验证年龄 200: {validate_age(200)}")
except InvalidAgeError as e:
    print(f"捕获异常：{e}")


# ========== 练习3：文件读写 ==========
print("\n=== 练习3：文本文件操作 ===")
"""
题目：编写函数处理文本文件
要求：
1. 函数 write_lines(filename, lines) 将字符串列表写入文件
2. 函数 read_lines(filename) 读取文件所有行并返回列表
3. 正确使用 with 语句管理文件资源
4. 使用 utf-8 编码
"""

def write_lines(filename, lines):
    """
    将字符串列表写入文件

    Args:
        filename: 文件名
        lines: 字符串列表
    """
    # TODO: 在这里实现你的代码
    pass


def read_lines(filename):
    """
    读取文件所有行

    Args:
        filename: 文件名

    Returns:
        list: 文件内容列表（去除换行符）
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
import os

test_file = "practice_test.txt"
test_data = ["第一行", "第二行", "第三行"]

write_lines(test_file, test_data)
result = read_lines(test_file)
print(f"写入数据：{test_data}")
print(f"读取数据：{result}")

# 清理文件
if os.path.exists(test_file):
    os.remove(test_file)


# ========== 练习4：JSON 数据处理 ==========
print("\n=== 练习4：JSON 学生信息管理 ===")
"""
题目：使用 JSON 管理学生信息
要求：
1. 函数 save_students(filename, students) 将学生列表保存为JSON
2. 函数 load_students(filename) 从JSON文件加载学生信息
3. JSON格式化输出（indent=2, ensure_ascii=False）
4. 处理文件不存在的情况（load时返回空列表）
"""

import json


def save_students(filename, students):
    """
    保存学生信息到JSON文件

    Args:
        filename: 文件名
        students: 学生信息列表
    """
    # TODO: 在这里实现你的代码
    pass


def load_students(filename):
    """
    从JSON文件加载学生信息

    Args:
        filename: 文件名

    Returns:
        list: 学生信息列表，文件不存在返回空列表
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
json_file = "students.json"

students = [
    {"name": "张三", "age": 20, "major": "计算机科学"},
    {"name": "李四", "age": 21, "major": "软件工程"},
    {"name": "王五", "age": 19, "major": "数据科学"}
]

save_students(json_file, students)
loaded = load_students(json_file)

print("保存的学生：")
for s in students:
    print(f"  {s['name']} - {s['major']}")

print("\n加载的学生：")
for s in loaded:
    print(f"  {s['name']} - {s['major']}")

# 清理文件
if os.path.exists(json_file):
    os.remove(json_file)


# ========== 练习5：CSV 数据处理 ==========
print("\n=== 练习5：CSV 商品管理 ===")
"""
题目：使用 CSV 管理商品信息
要求：
1. 函数 write_products_csv(filename, products) 将商品列表写入CSV
2. 函数 read_products_csv(filename) 从CSV读取商品信息
3. CSV包含表头：名称,价格,库存
4. 使用 DictReader 和 DictWriter
"""

import csv


def write_products_csv(filename, products):
    """
    将商品信息写入CSV文件

    Args:
        filename: 文件名
        products: 商品字典列表，包含 name, price, stock
    """
    # TODO: 在这里实现你的代码
    pass


def read_products_csv(filename):
    """
    从CSV文件读取商品信息

    Args:
        filename: 文件名

    Returns:
        list: 商品字典列表
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
csv_file = "products.csv"

products = [
    {"name": "笔记本电脑", "price": 5999, "stock": 50},
    {"name": "鼠标", "price": 99, "stock": 200},
    {"name": "键盘", "price": 299, "stock": 150}
]

write_products_csv(csv_file, products)
loaded_products = read_products_csv(csv_file)

print("商品信息：")
for p in loaded_products:
    print(f"  {p['name']}：¥{p['price']}，库存{p['stock']}")

# 清理文件
if os.path.exists(csv_file):
    os.remove(csv_file)


# ========== 练习6：综合练习 - 日志文件分析 ==========
print("\n=== 练习6：日志文件分析 ===")
"""
题目：编写函数分析日志文件
要求：
1. 函数 analyze_log(filename) 分析日志文件
2. 统计不同级别日志的数量（ERROR, WARNING, INFO）
3. 返回字典：{"ERROR": 数量, "WARNING": 数量, "INFO": 数量}
4. 处理文件不存在的异常
5. 忽略空行和注释行（#开头）
"""


def analyze_log(filename):
    """
    分析日志文件

    Args:
        filename: 日志文件名

    Returns:
        dict: 各级别日志数量统计
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
log_file = "test.log"

# 创建测试日志文件
log_content = """# 系统日志
ERROR: 数据库连接失败
WARNING: 内存使用率过高
INFO: 服务启动成功
ERROR: 文件未找到
INFO: 用户登录
WARNING: 磁盘空间不足
ERROR: 网络超时
INFO: 数据保存成功
"""

with open(log_file, "w", encoding="utf-8") as f:
    f.write(log_content)

# 分析日志
result = analyze_log(log_file)
print("日志统计：")
for level, count in result.items():
    print(f"  {level}: {count}条")

# 清理文件
if os.path.exists(log_file):
    os.remove(log_file)


# ========== 练习7：上下文管理器 ==========
print("\n=== 练习7：自定义上下文管理器 ===")
"""
题目：创建一个计时上下文管理器
要求：
1. 创建类 Timer，实现上下文管理器协议
2. 在 __enter__ 时记录开始时间
3. 在 __exit__ 时计算并打印执行时间
4. 可以使用 with Timer() 来测量代码块的执行时间
"""

import time


class Timer:
    """
    计时上下文管理器

    示例：
        with Timer():
            # 要计时的代码
            time.sleep(1)
    """

    def __enter__(self):
        """进入上下文"""
        # TODO: 在这里实现你的代码
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
print("测试计时器：")
with Timer():
    # 模拟耗时操作
    time.sleep(0.1)
    total = sum(range(1000000))


print("\n异常与文件基础练习完成！")
print("\n提示：完成所有TODO部分后，运行此文件查看结果")
