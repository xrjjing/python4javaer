#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：输入输出基础
完成以下练习：
"""

# 练习1：个人信息输出
print("=== 练习1：个人信息输出 ===")
# 依次从键盘输入姓名、年龄、城市
name = input("请输入姓名：")
age = input("请输入年龄：")
city = input("请输入城市：")

# 按格式输出：我是张三，今年25岁，来自北京
print(f"我是{name}，今年{age}岁，来自{city}。")

# 练习2：计算器
print("\n=== 练习2：简单计算器 ===")
num1 = float(input("请输入第一个数字："))
num2 = float(input("请输入第二个数字："))

print(f"\n{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num2 != 0 and num1 / num2 or '除数不能为0'}")

# 练习3：正方形计算
print("\n=== 练习3：正方形面积和周长 ===")
side = float(input("请输入正方形边长："))
area = side ** 2
perimeter = 4 * side

print(f"正方形面积：{area}")
print(f"正方形周长：{perimeter}")

# 练习4：思考题解答
print("\n=== 练习4：类型转换 ===")
text_number = "10"
print(f"字符串'{text_number}'的类型是：{type(text_number)}")
number = int(text_number)
print(f"转换为整数后：{number}，类型是：{type(number)}")
print(f"加5的结果：{number + 5}")

# 额外：布尔值运算
print("\n=== 额外：布尔值运算 ===")
print(f"True + True = {True + True}")  # 1 + 1 = 2
print(f"False + False = {False + False}")  # 0 + 0 = 0
print("因为True在Python中等价于1，False等价于0")
