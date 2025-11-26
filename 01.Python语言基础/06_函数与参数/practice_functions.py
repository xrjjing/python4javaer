#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：函数与参数
"""

# 练习1：基本函数
print("=== 练习1：基本函数 ===")
def is_even(n):
    """判断是否为偶数"""
    return n % 2 == 0

def is_odd(n):
    """判断是否为奇数"""
    return n % 2 != 0

print(f"4是偶数吗？{is_even(4)}")
print(f"5是奇数吗？{is_odd(5)}")

# 练习2：计算器函数
print("\n=== 练习2：计算器 ===")
def calculator(a, b, operator):
    """简单计算器"""
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b if b != 0 else "除数不能为0"
    else:
        return "无效运算符"

print(f"10 + 5 = {calculator(10, 5, '+')}")
print(f"10 - 5 = {calculator(10, 5, '-')}")
print(f"10 * 5 = {calculator(10, 5, '*')}")
print(f"10 / 5 = {calculator(10, 5, '/')}")

# 练习3：字符串处理函数
print("\n=== 练习3：字符串处理 ===")
def reverse_string(text):
    """反转字符串"""
    return text[::-1]

def count_vowels(text):
    """统计元音字母数量"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)

print(f"反转'Hello'：{reverse_string('Hello')}")
print(f"'Hello'中元音字母数：{count_vowels('Hello')}")

# 练习4：列表操作函数
print("\n=== 练习4：列表操作 ===")
def find_max(numbers):
    """找到列表中的最大值"""
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

def find_min(numbers):
    """找到列表中的最小值"""
    if not numbers:
        return None
    min_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
    return min_num

nums = [3, 7, 2, 9, 1, 8]
print(f"列表：{nums}")
print(f"最大值：{find_max(nums)}")
print(f"最小值：{find_min(nums)}")

# 练习5：可变参数函数
print("\n=== 练习5：可变参数 ===")
def average(*args):
    """计算平均值"""
    if not args:
        return 0
    return sum(args) / len(args)

print(f"平均分：{average(85, 92, 78, 90)}")

def print_info(name, **kwargs):
    """打印用户信息"""
    print(f"姓名：{name}")
    for key, value in kwargs.items():
        print(f"  {key}：{value}")

print_info("张三", 年龄=25, 城市="北京", 职业="工程师")

# 练习6：验证函数
print("\n=== 练习6：验证函数 ===")
def validate_email(email):
    """简单验证邮箱格式"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone):
    """简单验证手机号格式"""
    return phone.isdigit() and len(phone) == 11

emails = ["user@example.com", "invalid", "test@site"]
phones = ["13800138000", "123", "13800138001"]

print("邮箱验证：")
for email in emails:
    status = "有效" if validate_email(email) else "无效"
    print(f"  {email}：{status}")

print("\n手机号验证：")
for phone in phones:
    status = "有效" if validate_phone(phone) else "无效"
    print(f"  {phone}：{status}")

# 练习7：数据处理函数
print("\n=== 练习7：数据处理 ===")
def filter_positive(numbers):
    """过滤出正数"""
    return [n for n in numbers if n > 0]

def uppercase_all(strings):
    """将所有字符串转为大写"""
    return [s.upper() for s in strings]

nums = [-2, -1, 0, 1, 2, 3]
words = ["hello", "world", "python"]
print(f"正数：{filter_positive(nums)}")
print(f"大写：{uppercase_all(words)}")

# 练习8：装饰器示例
print("\n=== 练习8：装饰器 ===")
def logger(func):
    """日志装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数：{func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数结束：{func.__name__}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

result = add(5, 3)
print(f"结果：{result}")

# 练习9：斐波那契数列函数
print("\n=== 练习9：斐波那契 ===")
def fibonacci(n):
    """生成斐波那契数列前n项"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

print(f"前10项斐波那契数列：{fibonacci(10)}")

# 练习10：作用域练习
print("\n=== 练习10：作用域 ===")
count = 0  # 全局变量

def increment():
    global count
    count += 1
    return count

def decrement():
    global count
    count -= 1
    return count

print(f"初始值：{count}")
print(f"递增后：{increment()}")
print(f"递增后：{increment()}")
print(f"递减后：{decrement()}")
print(f"最终值：{count}")
