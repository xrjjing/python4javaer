#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
循环与迭代示例
演示：while循环、for循环、range、break、continue、嵌套循环
"""

# 1. while 循环
print("=== while 循环 ===")
count = 0
while count < 5:
    print(f"count = {count}")
    count += 1
print("循环结束")

# 2. while 循环计算累计和
print("\n=== 计算 1-10 的和 ===")
total = 0
num = 1
while num <= 10:
    total += num
    num += 1
print(f"1+2+...+10 = {total}")

# 3. for 循环与 range
print("\n=== for 循环与 range ===")
# 基本用法：range(stop)
print("range(5):")
for i in range(5):
    print(i, end=" ")
print()

# range(start, stop)
print("\nrange(2, 7):")
for i in range(2, 7):
    print(i, end=" ")
print()

# range(start, stop, step)
print("\nrange(0, 10, 2):")
for i in range(0, 10, 2):
    print(i, end=" ")
print()

# 4. 遍历列表
print("\n=== 遍历列表 ===")
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
for fruit in fruits:
    print(fruit)

# 使用 enumerate 获取索引
print("\n使用 enumerate:")
for idx, fruit in enumerate(fruits):
    print(f"{idx}: {fruit}")

# 5. 遍历字符串
print("\n=== 遍历字符串 ===")
text = "Python"
for char in text:
    print(char)

# 6. break 语句（提前退出循环）
print("\n=== break 语句 ===")
for i in range(10):
    if i == 5:
        print("遇到5，提前退出")
        break
    print(f"i = {i}")

# 7. continue 语句（跳过当前迭代）
print("\n=== continue 语句 ===")
for i in range(10):
    if i % 2 == 0:
        continue  # 跳过偶数
    print(f"奇数：{i}")

# 8. 嵌套循环
print("\n=== 嵌套循环 ===")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"i={i}, j={j}")

# 打印乘法表
print("\n=== 打印 5x5 乘法表 ===")
for i in range(1, 6):
    row = []
    for j in range(1, 6):
        row.append(f"{i*j:2d}")
    print(" ".join(row))

# 9. else 子句（循环正常结束时执行）
print("\n=== 循环的 else 子句 ===")
found = False
for i in range(5):
    if i == 10:
        found = True
        break
else:
    print("循环正常结束，未找到10")

# 10. 列表推导式（Pythonic 写法）
print("\n=== 列表推导式 ===")
# 传统循环
squares = []
for i in range(10):
    squares.append(i**2)
print(f"传统循环：{squares}")

# 列表推导式
squares2 = [i**2 for i in range(10)]
print(f"列表推导式：{squares2}")

# 带条件的列表推导式
even_squares = [i**2 for i in range(10) if i % 2 == 0]
print(f"偶数的平方：{even_squares}")

# 11. 遍历字典
print("\n=== 遍历字典 ===")
person = {"name": "张三", "age": 25, "city": "北京"}

# 遍历键
print("键：")
for key in person:
    print(key)

# 遍历值
print("值：")
for value in person.values():
    print(value)

# 遍历键值对
print("键值对：")
for key, value in person.items():
    print(f"{key}: {value}")

# 12. zip 函数（同时遍历多个序列）
print("\n=== 使用 zip ===")
names = ["张三", "李四", "王五"]
ages = [25, 30, 35]
cities = ["北京", "上海", "广州"]

for name, age, city in zip(names, ages, cities):
    print(f"{name}，{age}岁，来自{city}")
