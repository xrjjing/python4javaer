#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：变量、数据类型与运算符
"""

# 练习1：个人信息变量
print("=== 练习1：个人信息 ===")
# 定义变量：姓名、年龄、身高（米）、是否已婚
name = "张三"
age = 25
height = 1.80
is_married = False

# 输出格式：姓名：张三，年龄：25，身高：1.80，已婚：False
print(f"姓名：{name}，年龄：{age}，身高：{height}，已婚：{is_married}")

# 练习2：温度转换器
print("\n=== 练习2：温度转换 ===")
# 输入摄氏温度（字符串）
celsius_str = input("请输入摄氏温度：")
# 转换为浮点数
celsius = float(celsius_str)
# 计算华氏温度：F = C * 9 / 5 + 32
fahrenheit = celsius * 9 / 5 + 32
print(f"华氏温度：{fahrenheit:.2f}°F")

# 练习3：三位数分解
print("\n=== 练习3：三位数分解 ===")
number = int(input("请输入一个三位数："))
# 计算百位、十位、个位
hundreds = number // 100
tens = (number // 10) % 10
units = number % 10
print(f"百位：{hundreds}，十位：{tens}，个位：{units}")

# 验证
print(f"验证：{hundreds}*100 + {tens}*10 + {units} = {hundreds*100 + tens*10 + units}")

# 练习4：思考题 - 布尔值运算
print("\n=== 练习4：布尔值运算 ===")
print(f"True + True = {True + True}")  # 结果是 2
print(f"False + False = {False + False}")  # 结果是 0
print(f"True + False = {True + False}")  # 结果是 1
print("\n原因：在Python中，True等价于1，False等价于0")
print("这是Python的EAFP（ Easier to Ask for Forgiveness than Permission）风格的基础")

# 额外练习：比较运算
print("\n=== 额外练习：比较运算 ===")
a = 15
b = 20
c = 15

print(f"a = {a}, b = {b}, c = {c}")
print(f"a < b: {a < b}")        # True
print(f"a == c: {a == c}")      # True
print(f"a != b: {a != b}")      # True
print(f"a >= c: {a >= c}")      # True

# 练习5：逻辑运算应用
print("\n=== 练习5：逻辑运算 ===")
age = 20
has_license = True
has_car = False

print(f"年龄：{age}，有驾照：{has_license}，有车：{has_car}")
print(f"可以开车：{age >= 18 and has_license}")
print(f"需要考驾照：{age >= 18 and not has_license}")
print(f"有车但无驾照不能开：{has_car and not has_license}")
print(f"可以买车：{age >= 18 and has_license}")

# 练习6：运算符优先级
print("\n=== 练习6：运算符优先级 ===")
result1 = 10 + 5 * 2
result2 = (10 + 5) * 2
result3 = 10 ** 2 + 5
result4 = 10 ** (2 + 5)

print(f"10 + 5 * 2 = {result1}")          # 20 (先乘除后加减)
print(f"(10 + 5) * 2 = {result2}")        # 30 (括号优先)
print(f"10 ** 2 + 5 = {result3}")         # 105 (乘方比加减优先)
print(f"10 ** (2 + 5) = {result4}")       # 10000000 (括号内的先算)
