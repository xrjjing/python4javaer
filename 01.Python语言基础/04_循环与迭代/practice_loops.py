#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：循环与迭代
"""

# 练习1：打印九九乘法表
print("=== 练习1：九九乘法表 ===")
for i in range(1, 10):
    for j in range(1, i+1):
        print(f"{j}×{i}={i*j:2d}", end="  ")
    print()  # 换行

# 练习2：计算阶乘
print("\n=== 练习2：计算阶乘 ===")
n = int(input("请输入一个正整数："))
result = 1
for i in range(1, n+1):
    result *= i
print(f"{n}! = {result}")

# 练习3：斐波那契数列
print("\n=== 练习3：斐波那契数列 ===")
count = int(input("请输入要生成的数列长度："))
a, b = 0, 1
for _ in range(count):
    print(a, end=" ")
    a, b = b, a + b
print()

# 练习4：统计数字
print("\n=== 练习4：统计数字 ===")
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
count_greater_5 = 0
sum_numbers = 0

for num in numbers:
    sum_numbers += num
    if num > 5:
        count_greater_5 += 1

print(f"数字列表：{numbers}")
print(f"大于5的数字个数：{count_greater_5}")
print(f"所有数字的和：{sum_numbers}")
print(f"平均数：{sum_numbers / len(numbers):.2f}")

# 练习5：素数判断
print("\n=== 练习5：素数判断 ===")
num = int(input("请输入一个正整数："))

if num < 2:
    print(f"{num} 不是素数")
else:
    is_prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

    if is_prime:
        print(f"{num} 是素数")
    else:
        print(f"{num} 不是素数")

# 练习6：猜数字游戏
print("\n=== 练习6：猜数字游戏（1-100） ===")
import random
target = random.randint(1, 100)
attempts = 0

while True:
    guess = int(input("请输入猜测的数字："))
    attempts += 1

    if guess < target:
        print("太小了！")
    elif guess > target:
        print("太大了！")
    else:
        print(f"恭喜！猜对了！用了{attempts}次")
        break

# 练习7：打印三角形图案
print("\n=== 练习7：打印三角形 ===")
rows = 5
for i in range(1, rows + 1):
    # 打印空格
    print(" " * (rows - i), end="")
    # 打印星号
    print("*" * (2 * i - 1))

# 练习8：过滤列表中的偶数
print("\n=== 练习8：过滤偶数 ===")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = []

# 传统方法
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
print(f"原列表：{numbers}")
print(f"偶数列表：{even_numbers}")

# 列表推导式方法
even_numbers2 = [num for num in numbers if num % 2 == 0]
print(f"偶数列表（推导式）：{even_numbers2}")

# 练习9：遍历多个列表
print("\n=== 练习9：遍历多个列表 ===")
products = ["苹果", "香蕉", "橙子"]
prices = [3.5, 2.8, 4.2]
stocks = [100, 80, 120]

for product, price, stock in zip(products, prices, stocks):
    total_value = price * stock
    print(f"{product}：单价{price}元，库存{stock}，总价值{total_value:.2f}元")

# 练习10：使用 enumerate 统计
print("\n=== 练习10：统计字符出现位置 ===")
text = "hello python"
for index, char in enumerate(text):
    print(f"位置{index}：'{char}'")

# 练习11：生成杨辉三角
print("\n=== 练习11：杨辉三角 ===")
rows = 6
triangle = []

for i in range(rows):
    row = []
    for j in range(i + 1):
        if j == 0 or j == i:
            row.append(1)
        else:
            row.append(triangle[i-1][j-1] + triangle[i-1][j])
    triangle.append(row)

# 打印杨辉三角
for row in triangle:
    print(" ".join(map(str, row)).center(30))

# 练习12：死循环与 break（演示用，实际使用需谨慎）
print("\n=== 练习12：模拟 ATM 取款 ===")
balance = 1000
while True:
    print(f"当前余额：{balance}元")
    amount = int(input("请输入取款金额（0退出）："))
    if amount == 0:
        print("退出系统")
        break
    elif amount > balance:
        print("余额不足！")
    else:
        balance -= amount
        print(f"取款成功，剩余余额：{balance}元")
        if balance < 100:
            print("余额不足100元，请及时存款")
