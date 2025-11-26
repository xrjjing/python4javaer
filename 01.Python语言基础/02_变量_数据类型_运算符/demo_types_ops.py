#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变量、数据类型与运算符示例
演示：变量本质、常见数据类型、运算符用法
"""

# 1. 变量本质：绑定名称到对象
age = 28           # 将整数对象28绑定到变量名age
height = 1.75      # 浮点数
name = "Alice"     # 字符串
is_student = False # 布尔值

# type() 函数查看对象类型
print("=== 变量类型 ===")
print(f"age 的类型：{type(age)}")
print(f"height 的类型：{type(height)}")
print(f"name 的类型：{type(name)}")
print(f"is_student 的类型：{type(is_student)}")

# 2. 数值类型：int 和 float
print("\n=== 数值运算 ===")
year = 2025
birth_year = year - age  # 减法运算
print(f"出生年份：{birth_year}")

# Python中整数可以非常大
big_number = 10 ** 100
print(f"10的100次方：{big_number}")

# 浮点数精度
price = 19.99
print(f"价格：{price}，类型：{type(price)}")

# 3. 布尔类型：True 和 False
print("\n=== 布尔运算 ===")
print(f"年龄是否 >= 18：{age >= 18}")
print(f"是否是学生：{is_student}")
print(f"既是学生又满18岁：{is_student and age >= 18}")
print(f"不是学生：{not is_student}")

# 4. 字符串类型
print("\n=== 字符串操作 ===")
greeting = "Hello"
name = "World"
message = greeting + " " + name  # 字符串拼接
print(message)

# 字符串与数字不能直接相加
text_num = "10"
print(f"字符串'10' + 5 会报错，需要先转换")

# 5. 比较运算符
print("\n=== 比较运算 ===")
a = 10
b = 20
print(f"a = {a}, b = {b}")
print(f"a == b: {a == b}")
print(f"a != b: {a != b}")
print(f"a < b: {a < b}")
print(f"a > b: {a > b}")
print(f"a <= b: {a <= b}")
print(f"a >= b: {a >= b}")

# 6. 逻辑运算符
print("\n=== 逻辑运算 ===")
x = True
y = False
print(f"x = {x}, y = {y}")
print(f"x and y: {x and y}")  # False
print(f"x or y: {x or y}")    # True
print(f"not x: {not x}")      # False

# 7. 运算符优先级
print("\n=== 运算符优先级 ===")
result1 = 2 + 3 * 4          # 先乘除后加减
result2 = (2 + 3) * 4        # 括号优先
result3 = 2 ** 3 ** 2        # 右结合：2 ** (3 ** 2)
print(f"2 + 3 * 4 = {result1}")      # 14
print(f"(2 + 3) * 4 = {result2}")    # 20
print(f"2 ** 3 ** 2 = {result3}")    # 512

# 8. 类型转换
print("\n=== 类型转换 ===")
# 字符串转数字
text_number = "123"
num = int(text_number)
print(f"字符串'{text_number}'转整数：{num}")
print(f"类型：{type(num)}")

# 数字转字符串
age_int = 25
age_str = str(age_int)
print(f"整数{age_int}转字符串：'{age_str}'")
print(f"类型：{type(age_str)}")

# 数字转布尔
print(f"\n数字转布尔：")
print(f"bool(0): {bool(0)}")      # False
print(f"bool(1): {bool(1)}")      # True
print(f"bool(100): {bool(100)}")  # True
print(f"bool(-1): {bool(-1)}")    # True

# 空字符串转布尔
print(f"bool(''): {bool('')}")    # False
print(f"bool('hello'): {bool('hello')}")  # True

# 布尔转数字
print(f"\n布尔转数字：")
print(f"int(True): {int(True)}")  # 1
print(f"int(False): {int(False)}")  # 0
