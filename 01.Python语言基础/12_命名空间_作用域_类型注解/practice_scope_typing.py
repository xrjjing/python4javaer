#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命名空间、作用域与类型注解练习题
练习：LEGB规则、global/nonlocal、类型注解、泛型
"""

# ========== 练习1：作用域规则 ==========
print("=== 练习1：LEGB 作用域 ===")
"""
题目：理解和使用 LEGB 作用域规则
要求：
1. 创建全局变量 counter = 0
2. 创建函数 outer()，其中定义局部变量 counter = 10
3. 在 outer() 内创建嵌套函数 inner()，定义 counter = 20
4. inner() 打印自己的 counter
5. outer() 打印自己的 counter
6. 主程序打印全局的 counter
"""

# TODO: 在这里实现你的代码
pass

# 测试代码（取消注释）
# outer()
# print(f"全局 counter: {counter}")


# ========== 练习2：global 和 nonlocal ==========
print("\n=== 练习2：计数器实现 ===")
"""
题目：使用 global 和 nonlocal 实现计数器
要求：
1. 全局变量 total_count = 0
2. 函数 create_counter() 返回一个计数器函数
3. 计数器函数每次调用时：
   - 增加自己的内部计数（使用 nonlocal）
   - 增加全局计数（使用 global）
4. 返回当前计数
"""

total_count = 0


def create_counter():
    """
    创建计数器函数

    Returns:
        function: 计数器函数
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码（取消注释）
# counter1 = create_counter()
# counter2 = create_counter()
#
# print(f"counter1: {counter1()}")  # 1
# print(f"counter1: {counter1()}")  # 2
# print(f"counter2: {counter2()}")  # 1
# print(f"counter1: {counter1()}")  # 3
# print(f"全局总计数: {total_count}")


# ========== 练习3：基础类型注解 ==========
print("\n=== 练习3：类型注解函数 ===")
"""
题目：为函数添加完整的类型注解
要求：
1. 函数 calculate_bmi(weight, height) 计算BMI
   - 参数类型：float, float
   - 返回类型：float
2. 函数 format_name(first, last) 格式化姓名
   - 参数类型：str, str
   - 返回类型：str
3. 函数 is_adult(age) 判断是否成年
   - 参数类型：int
   - 返回类型：bool
"""


def calculate_bmi(weight, height):
    """
    计算BMI指数

    Args:
        weight: 体重（kg）
        height: 身高（m）

    Returns:
        BMI指数
    """
    # TODO: 添加类型注解并实现函数
    pass


def format_name(first, last):
    """
    格式化姓名

    Args:
        first: 名
        last: 姓

    Returns:
        完整姓名
    """
    # TODO: 添加类型注解并实现函数
    pass


def is_adult(age):
    """
    判断是否成年

    Args:
        age: 年龄

    Returns:
        是否成年（>=18）
    """
    # TODO: 添加类型注解并实现函数
    pass


# 测试代码（取消注释）
# print(f"BMI: {calculate_bmi(70.0, 1.75):.2f}")
# print(f"姓名: {format_name('三', '张')}")
# print(f"是否成年: {is_adult(20)}")


# ========== 练习4：容器类型注解 ==========
print("\n=== 练习4：数据处理函数 ===")
"""
题目：使用容器类型注解
要求：
1. 函数 filter_even_numbers(numbers: List[int]) -> List[int]
   过滤出偶数
2. 函数 merge_dicts(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]
   合并两个字典
3. 函数 get_unique_items(items: List[str]) -> Set[str]
   返回去重后的集合
4. 函数 find_user(user_id: int, users: List[Dict[str, any]]) -> Optional[Dict[str, any]]
   查找用户，找不到返回 None
"""

from typing import List, Dict, Set, Optional


def filter_even_numbers(numbers):
    """过滤偶数"""
    # TODO: 添加类型注解并实现函数
    pass


def merge_dicts(dict1, dict2):
    """合并字典"""
    # TODO: 添加类型注解并实现函数
    pass


def get_unique_items(items):
    """去重"""
    # TODO: 添加类型注解并实现函数
    pass


def find_user(user_id, users):
    """查找用户"""
    # TODO: 添加类型注解并实现函数
    pass


# 测试代码（取消注释）
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(f"偶数: {filter_even_numbers(numbers)}")
#
# d1 = {"a": 1, "b": 2}
# d2 = {"c": 3, "d": 4}
# print(f"合并字典: {merge_dicts(d1, d2)}")
#
# items = ["apple", "banana", "apple", "orange", "banana"]
# print(f"去重: {get_unique_items(items)}")
#
# users = [
#     {"id": 1, "name": "张三"},
#     {"id": 2, "name": "李四"},
#     {"id": 3, "name": "王五"}
# ]
# print(f"查找用户1: {find_user(1, users)}")
# print(f"查找用户99: {find_user(99, users)}")


# ========== 练习5：函数类型注解 ==========
print("\n=== 练习5：高阶函数 ===")
"""
题目：为高阶函数添加类型注解
要求：
1. 函数 apply_operation 接受两个整数和一个操作函数
   - 类型：(int, int, Callable[[int, int], int]) -> int
2. 函数 filter_by_condition 接受列表和条件函数
   - 类型：(List[T], Callable[[T], bool]) -> List[T]（使用泛型）
3. 实现示例操作函数和条件函数
"""

from typing import Callable, TypeVar

T = TypeVar('T')


def apply_operation(a, b, operation):
    """
    应用操作函数

    Args:
        a: 第一个整数
        b: 第二个整数
        operation: 操作函数

    Returns:
        操作结果
    """
    # TODO: 添加类型注解并实现函数
    pass


def filter_by_condition(items, condition):
    """
    根据条件过滤

    Args:
        items: 元素列表
        condition: 条件函数

    Returns:
        过滤后的列表
    """
    # TODO: 添加类型注解并实现函数
    pass


# 测试代码（取消注释）
# def add(x: int, y: int) -> int:
#     return x + y
#
# def multiply(x: int, y: int) -> int:
#     return x * y
#
# print(f"5 + 3 = {apply_operation(5, 3, add)}")
# print(f"5 * 3 = {apply_operation(5, 3, multiply)}")
#
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# evens = filter_by_condition(numbers, lambda x: x % 2 == 0)
# print(f"偶数: {evens}")
#
# words = ["apple", "cat", "banana", "dog", "elephant"]
# long_words = filter_by_condition(words, lambda w: len(w) > 4)
# print(f"长单词: {long_words}")


# ========== 练习6：泛型类 ==========
print("\n=== 练习6：泛型容器 ===")
"""
题目：创建泛型容器类 Box[T]
要求：
1. 使用 Generic[T] 创建泛型类
2. 属性 value: T 存储值
3. 方法 get() -> T 返回值
4. 方法 set(value: T) -> None 设置值
5. 方法 map(func: Callable[[T], U]) -> Box[U] 转换值
"""

from typing import Generic

U = TypeVar('U')


class Box(Generic[T]):
    """
    泛型盒子

    Attributes:
        value: 存储的值
    """

    def __init__(self, value):
        """
        初始化盒子

        Args:
            value: 初始值
        """
        # TODO: 添加类型注解并实现方法
        pass

    def get(self):
        """获取值"""
        # TODO: 添加类型注解并实现方法
        pass

    def set(self, value):
        """设置值"""
        # TODO: 添加类型注解并实现方法
        pass

    def map(self, func):
        """
        映射转换

        Args:
            func: 转换函数

        Returns:
            新的 Box 对象
        """
        # TODO: 添加类型注解并实现方法
        pass


# 测试代码（取消注释）
# # 整数盒子
# int_box: Box[int] = Box(42)
# print(f"整数盒子: {int_box.get()}")
#
# # 字符串盒子
# str_box: Box[str] = Box("Hello")
# print(f"字符串盒子: {str_box.get()}")
#
# # 映射转换
# squared_box = int_box.map(lambda x: x ** 2)
# print(f"平方后: {squared_box.get()}")
#
# length_box = str_box.map(lambda s: len(s))
# print(f"字符串长度: {length_box.get()}")


# ========== 练习7：类型注解的学生管理系统 ==========
print("\n=== 练习7：学生管理系统 ===")
"""
题目：创建带完整类型注解的学生管理系统
要求：
1. 创建 Student 类，包含类型注解：
   - name: str
   - age: int
   - grades: Dict[str, int]（科目->分数）
2. 方法 add_grade(subject: str, score: int) -> None
3. 方法 get_average() -> float
4. 方法 get_grade(subject: str) -> Optional[int]
5. 创建 StudentManager 类管理多个学生：
   - students: List[Student]
6. 方法 add_student(student: Student) -> None
7. 方法 find_student(name: str) -> Optional[Student]
8. 方法 get_top_students(n: int) -> List[Student]（按平均分）
"""


class Student:
    """学生类"""

    # TODO: 添加类属性的类型注解
    name = None
    age = None
    grades = None

    def __init__(self, name, age):
        """初始化学生"""
        # TODO: 添加类型注解并实现方法
        pass

    def add_grade(self, subject, score):
        """添加成绩"""
        # TODO: 添加类型注解并实现方法
        pass

    def get_average(self):
        """计算平均分"""
        # TODO: 添加类型注解并实现方法
        pass

    def get_grade(self, subject):
        """获取科目成绩"""
        # TODO: 添加类型注解并实现方法
        pass

    def __str__(self):
        """字符串表示"""
        return f"{self.name}({self.age}岁) - 平均分:{self.get_average():.1f}"


class StudentManager:
    """学生管理器"""

    def __init__(self):
        """初始化管理器"""
        # TODO: 添加类型注解并实现方法
        pass

    def add_student(self, student):
        """添加学生"""
        # TODO: 添加类型注解并实现方法
        pass

    def find_student(self, name):
        """查找学生"""
        # TODO: 添加类型注解并实现方法
        pass

    def get_top_students(self, n):
        """获取前N名学生"""
        # TODO: 添加类型注解并实现方法
        # 提示：使用 sorted() 和 lambda
        pass


# 测试代码（取消注释）
# manager = StudentManager()
#
# # 添加学生
# stu1 = Student("张三", 20)
# stu1.add_grade("数学", 90)
# stu1.add_grade("语文", 85)
# stu1.add_grade("英语", 88)
#
# stu2 = Student("李四", 21)
# stu2.add_grade("数学", 95)
# stu2.add_grade("语文", 92)
# stu2.add_grade("英语", 90)
#
# stu3 = Student("王五", 19)
# stu3.add_grade("数学", 78)
# stu3.add_grade("语文", 82)
# stu3.add_grade("英语", 75)
#
# manager.add_student(stu1)
# manager.add_student(stu2)
# manager.add_student(stu3)
#
# # 查找学生
# found = manager.find_student("张三")
# if found:
#     print(f"找到学生: {found}")
#     print(f"  数学成绩: {found.get_grade('数学')}")
#
# # 获取前2名
# print("\n前2名学生：")
# top_students = manager.get_top_students(2)
# for i, stu in enumerate(top_students, 1):
#     print(f"  {i}. {stu}")


# ========== 练习8：作用域陷阱 ==========
print("\n=== 练习8：修复作用域问题 ===")
"""
题目：修复以下代码中的作用域陷阱
问题代码：
    def create_multipliers():
        multipliers = []
        for i in range(3):
            multipliers.append(lambda x: x * i)
        return multipliers

    funcs = create_multipliers()
    print([f(2) for f in funcs])  # 期望 [0, 2, 4]，实际 [4, 4, 4]

要求：
1. 修复这个经典的闭包陷阱问题
2. 使用默认参数捕获循环变量的值
3. 结果应该是 [0, 2, 4]
"""


def create_multipliers():
    """
    创建乘法函数列表

    Returns:
        函数列表
    """
    # TODO: 修复闭包陷阱问题
    multipliers = []
    for i in range(3):
        multipliers.append(lambda x: x * i)
    return multipliers


# 测试代码（取消注释）
# funcs = create_multipliers()
# result = [f(2) for f in funcs]
# print(f"结果: {result}")
# print(f"期望: [0, 2, 4]")


print("\n命名空间、作用域与类型注解练习完成！")
print("\n提示：完成所有TODO部分后，取消注释测试代码运行")
print("      使用 mypy 可以检查类型注解：pip install mypy && mypy practice_scope_typing.py")
