#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数与参数示例
演示：def、返回值、位置参数、关键字参数、默认参数、*args、**kwargs
"""

# 1. 基本函数定义
print("=== 基本函数 ===")
def greet():
    print("你好！")

greet()

# 2. 带参数和返回值的函数
print("\n=== 带参数和返回值 ===")
def add(a, b):
    return a + b

result = add(5, 3)
print(f"add(5, 3) = {result}")

# 3. 位置参数
print("\n=== 位置参数 ===")
def describe_pet(animal, name):
    print(f"我有一只{animal}，它叫{name}")

describe_pet("猫", "咪咪")
describe_pet("狗", "旺财")

# 4. 关键字参数
print("\n=== 关键字参数 ===")
def describe_pet(name, animal, age):
    print(f"{name}是一只{animal}，{age}岁")

describe_pet(name="咪咪", animal="猫", age=2)
describe_pet(animal="狗", name="旺财", age=3)

# 5. 默认参数
print("\n=== 默认参数 ===")
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("张三")
greet("李四", "欢迎")

# 6. 混合使用位置和默认参数
print("\n=== 混合参数 ===")
def create_profile(name, age, city="北京", job="工程师"):
    print(f"姓名：{name}")
    print(f"年龄：{age}")
    print(f"城市：{city}")
    print(f"职业：{job}")

create_profile("张三", 25)
create_profile("李四", 30, "上海")
create_profile("王五", 28, job="医生")

# 7. *args（可变位置参数）
print("\n=== *args 可变参数 ===")
def sum_numbers(*args):
    total = 0
    for num in args:
        total += num
    return total

print(f"sum_numbers(1, 2, 3) = {sum_numbers(1, 2, 3)}")
print(f"sum_numbers(1, 2, 3, 4, 5) = {sum_numbers(1, 2, 3, 4, 5)}")

# 8. **kwargs（可变关键字参数）
print("\n=== **kwargs 可变关键字参数 ===")
def create_user(**kwargs):
    print("用户信息：")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

create_user(name="张三", age=25, email="zhang@example.com")

# 9. 同时使用 *args 和 **kwargs
print("\n=== *args 和 **kwargs 结合 ===")
def print_info(*args, **kwargs):
    print("位置参数：")
    for arg in args:
        print(f"  {arg}")
    print("关键字参数：")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info("参数1", "参数2", key1="值1", key2="值2")

# 10. 函数作为参数
print("\n=== 函数作为参数 ===")
def apply_operation(a, b, operation):
    return operation(a, b)

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(f"apply_operation(5, 3, add) = {apply_operation(5, 3, add)}")
print(f"apply_operation(5, 3, multiply) = {apply_operation(5, 3, multiply)}")

# 11. 作用域
print("\n=== 作用域 ===")
x = 10  # 全局变量

def test_scope():
    x = 20  # 局部变量
    print(f"函数内部 x = {x}")

test_scope()
print(f"函数外部 x = {x}")

# 12. 使用 global 关键字修改全局变量
print("\n=== 修改全局变量 ===")
counter = 0

def increment():
    global counter
    counter += 1
    print(f"计数器：{counter}")

increment()
increment()
print(f"最终计数器：{counter}")

# 13. 递归函数
print("\n=== 递归函数 ===")
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")

# 14. 匿名函数（lambda）
print("\n=== lambda 函数 ===")
square = lambda x: x ** 2
print(f"square(5) = {square(5)}")

add_func = lambda a, b: a + b
print(f"add_func(3, 4) = {add_func(3, 4)}")

# 15. 高阶函数
print("\n=== 高阶函数 ===")
numbers = [1, 2, 3, 4, 5]

# map 函数
squared = list(map(lambda x: x ** 2, numbers))
print(f"平方：{squared}")

# filter 函数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数：{evens}")

# reduce 函数
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print(f"总和：{total}")
