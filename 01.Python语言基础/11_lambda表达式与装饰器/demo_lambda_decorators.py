#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lambda表达式与装饰器示例
演示：匿名函数、高阶函数、装饰器基础、装饰器应用
"""

# 1. lambda 基础
print("=== lambda 基础 ===")
# 普通函数
def add(a, b):
    return a + b

# lambda 函数
add_lambda = lambda a, b: a + b

print(f"普通函数：add(3, 5) = {add(3, 5)}")
print(f"lambda函数：add_lambda(3, 5) = {add_lambda(3, 5)}")

# 2. lambda 在排序中的应用
print("\n=== lambda 在排序中的应用 ===")
students = [
    {"name": "张三", "age": 20, "score": 85},
    {"name": "李四", "age": 19, "score": 92},
    {"name": "王五", "age": 21, "score": 78},
]

# 按年龄排序
sorted_by_age = sorted(students, key=lambda x: x["age"])
print("按年龄排序：")
for s in sorted_by_age:
    print(f"  {s['name']}：{s['age']}岁")

# 按成绩排序（降序）
sorted_by_score = sorted(students, key=lambda x: x["score"], reverse=True)
print("\n按成绩排序（降序）：")
for s in sorted_by_score:
    print(f"  {s['name']}：{s['score']}分")

# 3. lambda 与 map、filter、reduce
print("\n=== lambda 与高阶函数 ===")
numbers = [1, 2, 3, 4, 5]

# map - 映射
squared = list(map(lambda x: x ** 2, numbers))
print(f"平方：{squared}")

# filter - 过滤
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数：{evens}")

# reduce - 归约
from functools import reduce
total = reduce(lambda x, y: x + y, numbers)
print(f"求和：{total}")

# 4. 简单装饰器
print("\n=== 简单装饰器 ===")
def my_decorator(func):
    """简单装饰器"""
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()

# 5. 带参数的装饰器
print("\n=== 带参数的装饰器 ===")
def logger(func):
    """日志装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数：{func.__name__}")
        print(f"参数：args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值：{result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

@logger
def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"

result1 = add(3, 5)
result2 = greet("张三", greeting="欢迎")

# 6. 计时装饰器
print("\n=== 计时装饰器 ===")
import time

def timer(func):
    """计时装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间：{end - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    """模拟耗时操作"""
    time.sleep(0.1)
    return "完成"

result = slow_function()

# 7. 缓存装饰器
print("\n=== 缓存装饰器 ===")
def memoize(func):
    """缓存装饰器"""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            print(f"计算 {args}")
            cache[args] = func(*args)
        else:
            print(f"使用缓存 {args}")
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    """斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"fibonacci(5) = {fibonacci(5)}")
print(f"fibonacci(5) = {fibonacci(5)}")  # 使用缓存

# 8. 多个装饰器叠加
print("\n=== 多个装饰器叠加 ===")
def bold(func):
    """加粗装饰器"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<b>{result}</b>"
    return wrapper

def italic(func):
    """斜体装饰器"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<i>{result}</i>"
    return wrapper

@bold
@italic
def get_text():
    return "Hello, World!"

print(get_text())

# 9. 带参数的装饰器
print("\n=== 带参数的装饰器 ===")
def repeat(times):
    """重复执行装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()

# 10. 类装饰器
print("\n=== 类装饰器 ===")
class Counter:
    """计数装饰器"""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用次数：{self.count}")
        return self.func(*args, **kwargs)

@Counter
def process():
    print("处理中...")

process()
process()
process()

# 11. functools.wraps 保留元信息
print("\n=== 保留函数元信息 ===")
from functools import wraps

def my_decorator_with_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """包装函数"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator_with_wraps
def documented_function():
    """这是一个有文档的函数"""
    pass

print(f"函数名：{documented_function.__name__}")
print(f"文档：{documented_function.__doc__}")

# 12. 实用装饰器示例
print("\n=== 实用装饰器示例 ===")

# 权限检查装饰器
def require_auth(func):
    """权限检查装饰器"""
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated"):
            print("错误：需要登录")
            return None
        return func(user, *args, **kwargs)
    return wrapper

@require_auth
def delete_user(user, user_id):
    print(f"删除用户：{user_id}")
    return True

# 测试
user1 = {"name": "张三", "is_authenticated": True}
user2 = {"name": "李四", "is_authenticated": False}

delete_user(user1, 123)
delete_user(user2, 456)

# 13. 单例模式装饰器
print("\n=== 单例模式装饰器 ===")
def singleton(cls):
    """单例装饰器"""
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("初始化数据库连接")

db1 = Database()
db2 = Database()
print(f"db1 和 db2 是同一个对象：{db1 is db2}")

# 14. 属性装饰器
print("\n=== 属性装饰器 ===")
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """获取半径"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """设置半径"""
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value

    @property
    def area(self):
        """计算面积"""
        import math
        return math.pi * self._radius ** 2

circle = Circle(5)
print(f"半径：{circle.radius}")
print(f"面积：{circle.area:.2f}")

circle.radius = 10
print(f"新半径：{circle.radius}")
print(f"新面积：{circle.area:.2f}")

# 15. 静态方法和类方法装饰器
print("\n=== 静态方法和类方法 ===")
class MathUtils:
    PI = 3.14159

    @staticmethod
    def add(a, b):
        """静态方法"""
        return a + b

    @classmethod
    def circle_area(cls, radius):
        """类方法"""
        return cls.PI * radius ** 2

print(f"静态方法：add(3, 5) = {MathUtils.add(3, 5)}")
print(f"类方法：circle_area(5) = {MathUtils.circle_area(5):.2f}")

print("\nlambda 和装饰器演示完成！")
