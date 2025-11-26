#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面向对象入门示例
演示：class、__init__、实例方法、属性、继承
"""

# 1. 基本类定义
print("=== 基本类定义 ===")
class Dog:
    """狗类"""
    def __init__(self, name, age):
        """初始化方法"""
        self.name = name
        self.age = age

    def bark(self):
        """吠叫方法"""
        print(f"{self.name}在叫：汪汪汪！")

    def get_info(self):
        """获取信息"""
        return f"{self.name}，{self.age}岁"

# 创建实例
dog1 = Dog("旺财", 3)
dog2 = Dog("小黑", 2)

print(dog1.get_info())
dog1.bark()
print(dog2.get_info())
dog2.bark()

# 2. 类属性和实例属性
print("\n=== 类属性和实例属性 ===")
class Student:
    """学生类"""
    school = "清华大学"  # 类属性

    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age

    def introduce(self):
        print(f"我是{self.name}，{self.age}岁，来自{Student.school}")

stu1 = Student("张三", 20)
stu2 = Student("李四", 21)

stu1.introduce()
stu2.introduce()

# 修改类属性
Student.school = "北京大学"
stu1.introduce()
stu2.introduce()

# 3. 私有属性和方法
print("\n=== 私有属性和方法 ===")
class BankAccount:
    """银行账户类"""
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # 私有属性

    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.__balance += amount
            print(f"存款{amount}元成功，余额：{self.__balance}元")

    def withdraw(self, amount):
        """取款"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"取款{amount}元成功，余额：{self.__balance}元")
        else:
            print("余额不足或金额无效")

    def get_balance(self):
        """获取余额"""
        return self.__balance

account = BankAccount("张三", 1000)
account.deposit(500)
account.withdraw(300)
print(f"当前余额：{account.get_balance()}元")

# 4. 继承
print("\n=== 继承 ===")
class Animal:
    """动物基类"""
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name}发出声音")

class Cat(Animal):
    """猫类，继承自Animal"""
    def speak(self):
        print(f"{self.name}说：喵喵喵")

class Dog(Animal):
    """狗类，继承自Animal"""
    def speak(self):
        print(f"{self.name}说：汪汪汪")

cat = Cat("咪咪")
dog = Dog("旺财")

cat.speak()
dog.speak()

# 5. super() 调用父类方法
print("\n=== super() 调用父类 ===")
class Person:
    """人类"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"我是{self.name}，{self.age}岁")

class Employee(Person):
    """员工类"""
    def __init__(self, name, age, job_title):
        super().__init__(name, age)  # 调用父类初始化
        self.job_title = job_title

    def introduce(self):
        super().introduce()  # 调用父类方法
        print(f"我的职位是{self.job_title}")

emp = Employee("张三", 30, "软件工程师")
emp.introduce()

# 6. 类方法和静态方法
print("\n=== 类方法和静态方法 ===")
class MathUtils:
    """数学工具类"""
    PI = 3.14159

    @classmethod
    def circle_area(cls, radius):
        """类方法：计算圆面积"""
        return cls.PI * radius ** 2

    @staticmethod
    def add(a, b):
        """静态方法：加法"""
        return a + b

print(f"圆面积：{MathUtils.circle_area(5)}")
print(f"加法：{MathUtils.add(3, 4)}")

# 7. 特殊方法（魔术方法）
print("\n=== 特殊方法 ===")
class Point:
    """点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """字符串表示"""
        return f"Point({self.x}, {self.y})"

    def __add__(self, other):
        """加法运算符重载"""
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """相等运算符重载"""
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2

print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p1 + p2: {p3}")
print(f"p1 == p2: {p1 == p2}")

# 8. 属性装饰器
print("\n=== 属性装饰器 ===")
class Temperature:
    """温度类"""
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """获取摄氏温度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏温度"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):
        """获取华氏温度"""
        return self._celsius * 9/5 + 32

temp = Temperature(25)
print(f"摄氏温度：{temp.celsius}°C")
print(f"华氏温度：{temp.fahrenheit}°F")

temp.celsius = 30
print(f"修改后摄氏温度：{temp.celsius}°C")
print(f"修改后华氏温度：{temp.fahrenheit}°F")
