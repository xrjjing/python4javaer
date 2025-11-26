#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lambda表达式与装饰器练习题
练习：匿名函数、高阶函数、装饰器、缓存、权限控制
"""

# ========== 练习1：lambda 基础 ==========
print("=== 练习1：lambda 表达式 ===")
"""
题目：使用 lambda 完成以下任务
要求：
1. 创建 lambda 函数计算两数之积
2. 创建 lambda 函数判断数字是否是偶数
3. 创建 lambda 函数获取字典的指定键值
4. 使用这些 lambda 函数处理数据
"""

# TODO: 在这里实现你的代码
# multiply = lambda ...
# is_even = lambda ...
# get_name = lambda ...

# 测试代码（取消注释）
# print(f"5 * 3 = {multiply(5, 3)}")
# print(f"4 是偶数：{is_even(4)}")
# print(f"7 是偶数：{is_even(7)}")
# person = {"name": "张三", "age": 25}
# print(f"姓名：{get_name(person)}")


# ========== 练习2：lambda 与高阶函数 ==========
print("\n=== 练习2：数据处理 ===")
"""
题目：使用 lambda、map、filter、reduce 处理数据
要求：
1. 使用 map 和 lambda 将温度列表从摄氏度转换为华氏度 (F = C * 9/5 + 32)
2. 使用 filter 和 lambda 筛选出及格的分数（>=60）
3. 使用 reduce 和 lambda 计算列表所有元素的乘积
4. 对学生列表按成绩降序排序（使用 sorted 和 lambda）
"""

from functools import reduce

# 数据
celsius_temps = [0, 10, 20, 30, 40]
scores = [45, 78, 92, 55, 88, 67, 34, 90]
numbers = [2, 3, 4, 5]
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
    {"name": "赵六", "score": 95}
]

# TODO: 在这里实现你的代码
# fahrenheit_temps = list(map(...))
# passed_scores = list(filter(...))
# product = reduce(...)
# sorted_students = sorted(...)

# 测试代码（取消注释）
# print(f"摄氏温度：{celsius_temps}")
# print(f"华氏温度：{fahrenheit_temps}")
# print(f"\n所有分数：{scores}")
# print(f"及格分数：{passed_scores}")
# print(f"\n数字列表：{numbers}")
# print(f"所有数字的乘积：{product}")
# print("\n学生排名：")
# for i, s in enumerate(sorted_students, 1):
#     print(f"  {i}. {s['name']}: {s['score']}分")


# ========== 练习3：基础装饰器 ==========
print("\n=== 练习3：日志装饰器 ===")
"""
题目：创建一个日志装饰器 log_function
要求：
1. 装饰器在函数执行前打印 "调用函数: 函数名"
2. 装饰器在函数执行后打印 "函数返回: 返回值"
3. 使用 functools.wraps 保留函数元信息
4. 应用到示例函数上
"""

from functools import wraps


def log_function(func):
    """
    日志装饰器

    Args:
        func: 被装饰的函数

    Returns:
        装饰后的函数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（取消注释装饰器）
# @log_function
def add(a, b):
    """计算两数之和"""
    return a + b


# @log_function
def greet(name):
    """问候函数"""
    return f"你好，{name}！"


# 测试（取消注释）
# result1 = add(3, 5)
# result2 = greet("张三")


# ========== 练习4：计时装饰器 ==========
print("\n=== 练习4：性能计时 ===")
"""
题目：创建计时装饰器 timing
要求：
1. 记录函数执行的开始和结束时间
2. 打印函数执行耗时（秒）
3. 支持任意参数的函数
4. 返回函数的原始返回值
"""

import time


def timing(func):
    """
    计时装饰器

    Args:
        func: 被装饰的函数

    Returns:
        装饰后的函数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（取消注释装饰器）
# @timing
def slow_sum(n):
    """计算1到n的和（模拟慢速操作）"""
    time.sleep(0.1)  # 模拟耗时
    return sum(range(n + 1))


# @timing
def fast_multiply(a, b):
    """快速乘法"""
    return a * b


# 测试（取消注释）
# result1 = slow_sum(100)
# print(f"结果：{result1}")
# result2 = fast_multiply(123, 456)
# print(f"结果：{result2}")


# ========== 练习5：缓存装饰器 ==========
print("\n=== 练习5：结果缓存 ===")
"""
题目：创建缓存装饰器 cache
要求：
1. 将函数的参数和返回值存储在字典中
2. 相同参数第二次调用时直接返回缓存结果
3. 打印是否使用了缓存
4. 用于优化递归的斐波那契函数
"""


def cache(func):
    """
    缓存装饰器

    Args:
        func: 被装饰的函数

    Returns:
        装饰后的函数
    """
    # TODO: 在这里实现你的代码
    # 提示：使用闭包变量存储缓存字典
    pass


# 测试代码（取消注释装饰器）
# @cache
def fibonacci(n):
    """计算斐波那契数（递归）"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# @cache
def expensive_calculation(x, y):
    """模拟耗时计算"""
    print(f"  执行计算：{x} + {y}")
    time.sleep(0.1)
    return x + y


# 测试（取消注释）
# print("斐波那契数列：")
# print(f"fibonacci(10) = {fibonacci(10)}")
# print(f"fibonacci(10) = {fibonacci(10)}")  # 使用缓存
#
# print("\n耗时计算：")
# print(f"结果：{expensive_calculation(5, 3)}")
# print(f"结果：{expensive_calculation(5, 3)}")  # 使用缓存
# print(f"结果：{expensive_calculation(5, 3)}")  # 使用缓存


# ========== 练习6：带参数的装饰器 ==========
print("\n=== 练习6：重复执行装饰器 ===")
"""
题目：创建带参数的装饰器 repeat(times)
要求：
1. 装饰器接受参数 times，指定函数执行次数
2. 返回最后一次执行的结果
3. 这是一个装饰器工厂（三层嵌套）
4. 支持 @repeat(3) 这样的语法
"""


def repeat(times):
    """
    重复执行装饰器工厂

    Args:
        times: 重复次数

    Returns:
        装饰器函数
    """
    # TODO: 在这里实现你的代码
    # 提示：需要三层嵌套函数
    pass


# 测试代码（取消注释装饰器）
# @repeat(3)
def say_hello(name):
    """问候函数"""
    print(f"你好，{name}！")
    return f"问候了{name}"


# @repeat(5)
def print_number(n):
    """打印数字"""
    print(n, end=" ")
    return n


# 测试（取消注释）
# result = say_hello("张三")
# print(f"返回值：{result}\n")
# print("数字：")
# result = print_number(42)
# print(f"\n返回值：{result}")


# ========== 练习7：权限检查装饰器 ==========
print("\n=== 练习7：权限控制 ===")
"""
题目：创建权限检查装饰器 require_permission(permission)
要求：
1. 装饰器接受所需权限作为参数
2. 被装饰的函数第一个参数必须是 user 字典
3. user 字典包含 'permissions' 键（权限列表）
4. 如果用户没有所需权限，打印错误并返回 None
5. 如果有权限，正常执行函数
"""


def require_permission(permission):
    """
    权限检查装饰器工厂

    Args:
        permission: 所需权限

    Returns:
        装饰器函数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（取消注释装饰器）
# @require_permission("admin")
def delete_user(user, user_id):
    """删除用户（需要admin权限）"""
    print(f"删除用户：{user_id}")
    return True


# @require_permission("write")
def create_post(user, title, content):
    """创建文章（需要write权限）"""
    print(f"创建文章：{title}")
    return {"title": title, "content": content}


# 测试（取消注释）
# admin_user = {"name": "管理员", "permissions": ["read", "write", "admin"]}
# normal_user = {"name": "普通用户", "permissions": ["read"]}
#
# print("管理员删除用户：")
# delete_user(admin_user, 123)
#
# print("\n普通用户删除用户：")
# delete_user(normal_user, 456)
#
# print("\n普通用户创建文章：")
# create_post(normal_user, "标题", "内容")


# ========== 练习8：类装饰器 ==========
print("\n=== 练习8：调用计数器 ===")
"""
题目：创建类装饰器 CallCounter
要求：
1. 使用类实现装饰器（实现 __init__ 和 __call__）
2. 记录函数被调用的次数
3. 提供 get_count() 方法返回调用次数
4. 每次调用时打印当前调用次数
"""


class CallCounter:
    """
    调用计数器装饰器

    Attributes:
        func: 被装饰的函数
        count: 调用次数
    """

    def __init__(self, func):
        """
        初始化装饰器

        Args:
            func: 被装饰的函数
        """
        # TODO: 在这里实现你的代码
        pass

    def __call__(self, *args, **kwargs):
        """
        调用被装饰的函数

        Args:
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            函数返回值
        """
        # TODO: 在这里实现你的代码
        pass

    def get_count(self):
        """
        获取调用次数

        Returns:
            int: 调用次数
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码（取消注释装饰器）
# @CallCounter
def process_data(data):
    """处理数据"""
    return len(data)


# @CallCounter
def calculate(x, y):
    """计算"""
    return x + y


# 测试（取消注释）
# process_data([1, 2, 3])
# process_data([4, 5])
# process_data([6, 7, 8, 9])
# print(f"process_data 被调用了 {process_data.get_count()} 次")
#
# calculate(1, 2)
# calculate(3, 4)
# print(f"calculate 被调用了 {calculate.get_count()} 次")


# ========== 练习9：综合练习 - 单例装饰器 ==========
print("\n=== 练习9：单例模式 ===")
"""
题目：创建单例装饰器 singleton
要求：
1. 装饰一个类，使其只能创建一个实例
2. 多次实例化返回同一个对象
3. 使用字典存储实例
4. 测试 Database 类
"""


def singleton(cls):
    """
    单例装饰器

    Args:
        cls: 被装饰的类

    Returns:
        获取实例的函数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（取消注释装饰器）
# @singleton
class Database:
    """数据库连接类"""

    def __init__(self, host="localhost"):
        """初始化数据库连接"""
        print(f"创建数据库连接：{host}")
        self.host = host
        self.connected = True

    def query(self, sql):
        """执行查询"""
        return f"执行查询：{sql}"


# @singleton
class Config:
    """配置类"""

    def __init__(self):
        """初始化配置"""
        print("加载配置文件")
        self.settings = {}

    def get(self, key):
        """获取配置"""
        return self.settings.get(key)


# 测试（取消注释）
# print("创建第一个数据库实例：")
# db1 = Database()
# print("\n创建第二个数据库实例：")
# db2 = Database()
# print(f"\ndb1 和 db2 是同一个对象：{db1 is db2}")
# print(f"db1.query: {db1.query('SELECT * FROM users')}")
#
# print("\n创建配置实例：")
# config1 = Config()
# config2 = Config()
# print(f"config1 和 config2 是同一个对象：{config1 is config2}")


print("\nlambda表达式与装饰器练习完成！")
print("\n提示：完成所有TODO部分后，取消注释测试代码运行")
