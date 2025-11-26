#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面向对象入门练习题
练习：类定义、继承、多态、特殊方法、属性装饰器
"""

# ========== 练习1：基本类定义 ==========
print("=== 练习1：图书类 ===")
"""
题目：创建一个图书类 Book
要求：
1. 包含属性：title（书名）、author（作者）、price（价格）、isbn（ISBN号）
2. 实现 __init__ 方法初始化这些属性
3. 实现 get_info() 方法，返回图书信息字符串
4. 实现 apply_discount(discount) 方法，应用折扣（0-1之间的小数）
"""


class Book:
    """图书类"""

    def __init__(self, title, author, price, isbn):
        """
        初始化图书

        Args:
            title: 书名
            author: 作者
            price: 价格
            isbn: ISBN号
        """
        # TODO: 在这里实现你的代码
        pass

    def get_info(self):
        """
        获取图书信息

        Returns:
            str: 图书信息字符串
        """
        # TODO: 在这里实现你的代码
        pass

    def apply_discount(self, discount):
        """
        应用折扣

        Args:
            discount: 折扣率（0-1之间）

        Returns:
            float: 折扣后的价格
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码
book = Book("Python编程", "张三", 89.0, "978-7-111-12345-6")
print(book.get_info())
new_price = book.apply_discount(0.8)
print(f"8折后价格：¥{new_price:.2f}")


# ========== 练习2：类属性和实例属性 ==========
print("\n=== 练习2：员工类 ===")
"""
题目：创建员工类 Employee
要求：
1. 类属性 company = "科技有限公司"
2. 类属性 employee_count = 0（记录员工总数）
3. 实例属性：name（姓名）、position（职位）、salary（薪资）
4. 每创建一个员工，employee_count 自动加1
5. 实现类方法 get_employee_count() 返回员工总数
"""


class Employee:
    """员工类"""

    company = "科技有限公司"
    employee_count = 0

    def __init__(self, name, position, salary):
        """
        初始化员工

        Args:
            name: 姓名
            position: 职位
            salary: 薪资
        """
        # TODO: 在这里实现你的代码
        pass

    @classmethod
    def get_employee_count(cls):
        """
        获取员工总数

        Returns:
            int: 员工总数
        """
        # TODO: 在这里实现你的代码
        pass

    def get_info(self):
        """获取员工信息"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
emp1 = Employee("张三", "工程师", 15000)
emp2 = Employee("李四", "经理", 20000)
emp3 = Employee("王五", "设计师", 12000)

print(f"公司：{Employee.company}")
print(f"员工总数：{Employee.get_employee_count()}")
print(emp1.get_info())


# ========== 练习3：私有属性和封装 ==========
print("\n=== 练习3：银行账户 ===")
"""
题目：创建银行账户类 BankAccount
要求：
1. 私有属性 __balance（余额）
2. 构造函数设置初始余额和账户持有人姓名
3. 实现 deposit(amount) 存款方法
4. 实现 withdraw(amount) 取款方法（余额不足时拒绝）
5. 实现 get_balance() 获取余额
6. 余额只能通过方法修改，不能直接访问
"""


class BankAccount:
    """银行账户类"""

    def __init__(self, owner, initial_balance=0):
        """
        初始化账户

        Args:
            owner: 账户持有人
            initial_balance: 初始余额
        """
        # TODO: 在这里实现你的代码
        pass

    def deposit(self, amount):
        """
        存款

        Args:
            amount: 存款金额
        """
        # TODO: 在这里实现你的代码
        pass

    def withdraw(self, amount):
        """
        取款

        Args:
            amount: 取款金额

        Returns:
            bool: 取款是否成功
        """
        # TODO: 在这里实现你的代码
        pass

    def get_balance(self):
        """
        获取余额

        Returns:
            float: 当前余额
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码
account = BankAccount("张三", 1000)
print(f"初始余额：¥{account.get_balance()}")
account.deposit(500)
print(f"存款后余额：¥{account.get_balance()}")
account.withdraw(300)
print(f"取款后余额：¥{account.get_balance()}")
account.withdraw(2000)  # 余额不足


# ========== 练习4：继承和方法重写 ==========
print("\n=== 练习4：形状继承 ===")
"""
题目：创建形状类的继承体系
要求：
1. 基类 Shape，包含 area() 和 perimeter() 方法（返回0）
2. 子类 Rectangle（矩形），重写这两个方法
3. 子类 Circle（圆形），重写这两个方法
4. 使用 super() 调用父类的 __init__ 方法
5. 圆周率使用 3.14159
"""


class Shape:
    """形状基类"""

    def __init__(self, name):
        """
        初始化形状

        Args:
            name: 形状名称
        """
        # TODO: 在这里实现你的代码
        pass

    def area(self):
        """计算面积"""
        return 0

    def perimeter(self):
        """计算周长"""
        return 0


class Rectangle(Shape):
    """矩形类"""

    def __init__(self, width, height):
        """
        初始化矩形

        Args:
            width: 宽度
            height: 高度
        """
        # TODO: 在这里实现你的代码
        pass

    def area(self):
        """计算矩形面积"""
        # TODO: 在这里实现你的代码
        pass

    def perimeter(self):
        """计算矩形周长"""
        # TODO: 在这里实现你的代码
        pass


class Circle(Shape):
    """圆形类"""

    PI = 3.14159

    def __init__(self, radius):
        """
        初始化圆形

        Args:
            radius: 半径
        """
        # TODO: 在这里实现你的代码
        pass

    def area(self):
        """计算圆形面积"""
        # TODO: 在这里实现你的代码
        pass

    def perimeter(self):
        """计算圆形周长"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
rect = Rectangle(5, 3)
circle = Circle(4)

print(f"矩形：面积={rect.area()}, 周长={rect.perimeter()}")
print(f"圆形：面积={circle.area():.2f}, 周长={circle.perimeter():.2f}")


# ========== 练习5：特殊方法（魔术方法） ==========
print("\n=== 练习5：商品类 ===")
"""
题目：创建商品类 Product，实现特殊方法
要求：
1. 属性：name（名称）、price（价格）、quantity（数量）
2. 实现 __str__ 方法，返回易读的字符串表示
3. 实现 __repr__ 方法，返回详细的对象表示
4. 实现 __eq__ 方法，比较两个商品是否相同（名称相同即可）
5. 实现 __lt__ 方法，按价格比较大小
"""


class Product:
    """商品类"""

    def __init__(self, name, price, quantity):
        """
        初始化商品

        Args:
            name: 名称
            price: 价格
            quantity: 数量
        """
        # TODO: 在这里实现你的代码
        pass

    def __str__(self):
        """字符串表示"""
        # TODO: 在这里实现你的代码
        pass

    def __repr__(self):
        """详细表示"""
        # TODO: 在这里实现你的代码
        pass

    def __eq__(self, other):
        """相等比较"""
        # TODO: 在这里实现你的代码
        pass

    def __lt__(self, other):
        """小于比较"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
p1 = Product("笔记本", 5999, 10)
p2 = Product("鼠标", 99, 50)
p3 = Product("笔记本", 5999, 5)

print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p1 == p3: {p1 == p3}")  # 名称相同
print(f"p1 < p2: {p1 < p2}")    # 按价格比较

# 排序
products = [p1, p2, p3]
sorted_products = sorted(products)
print("按价格排序：")
for p in sorted_products:
    print(f"  {p}")


# ========== 练习6：属性装饰器 ==========
print("\n=== 练习6：温度转换 ===")
"""
题目：创建温度类 Temperature，使用属性装饰器
要求：
1. 私有属性 _celsius 存储摄氏温度
2. 使用 @property 装饰器创建 celsius 属性（getter）
3. 使用 @celsius.setter 装饰器创建 celsius 属性（setter）
4. setter 中检查温度不能低于 -273.15（绝对零度）
5. 使用 @property 创建只读属性 fahrenheit（华氏温度）
6. 使用 @property 创建只读属性 kelvin（开尔文温度）
"""


class Temperature:
    """温度类"""

    def __init__(self, celsius):
        """
        初始化温度

        Args:
            celsius: 摄氏温度
        """
        # TODO: 在这里实现你的代码
        pass

    @property
    def celsius(self):
        """获取摄氏温度"""
        # TODO: 在这里实现你的代码
        pass

    @celsius.setter
    def celsius(self, value):
        """
        设置摄氏温度

        Args:
            value: 摄氏温度值

        Raises:
            ValueError: 温度低于绝对零度
        """
        # TODO: 在这里实现你的代码
        pass

    @property
    def fahrenheit(self):
        """
        获取华氏温度

        Returns:
            float: 华氏温度 (C * 9/5 + 32)
        """
        # TODO: 在这里实现你的代码
        pass

    @property
    def kelvin(self):
        """
        获取开尔文温度

        Returns:
            float: 开尔文温度 (C + 273.15)
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码
temp = Temperature(25)
print(f"摄氏温度：{temp.celsius}°C")
print(f"华氏温度：{temp.fahrenheit:.2f}°F")
print(f"开尔文温度：{temp.kelvin:.2f}K")

temp.celsius = 100
print(f"\n修改后：")
print(f"摄氏温度：{temp.celsius}°C")
print(f"华氏温度：{temp.fahrenheit:.2f}°F")

try:
    temp.celsius = -300  # 低于绝对零度
except ValueError as e:
    print(f"错误：{e}")


# ========== 练习7：静态方法和类方法 ==========
print("\n=== 练习7：日期工具类 ===")
"""
题目：创建日期类 Date，使用静态方法和类方法
要求：
1. 属性：year, month, day
2. 实现静态方法 is_leap_year(year) 判断是否是闰年
3. 实现类方法 from_string(date_string) 从字符串创建日期（格式：YYYY-MM-DD）
4. 实现实例方法 format() 返回格式化的日期字符串
"""


class Date:
    """日期类"""

    def __init__(self, year, month, day):
        """
        初始化日期

        Args:
            year: 年
            month: 月
            day: 日
        """
        # TODO: 在这里实现你的代码
        pass

    @staticmethod
    def is_leap_year(year):
        """
        判断是否是闰年

        Args:
            year: 年份

        Returns:
            bool: 是否是闰年
        """
        # TODO: 在这里实现你的代码
        # 提示：能被4整除但不能被100整除，或者能被400整除
        pass

    @classmethod
    def from_string(cls, date_string):
        """
        从字符串创建日期对象

        Args:
            date_string: 日期字符串（格式：YYYY-MM-DD）

        Returns:
            Date: 日期对象
        """
        # TODO: 在这里实现你的代码
        pass

    def format(self):
        """
        格式化日期

        Returns:
            str: 格式化的日期字符串（如：2024年1月1日）
        """
        # TODO: 在这里实现你的代码
        pass


# 测试代码
date1 = Date(2024, 1, 1)
print(date1.format())

date2 = Date.from_string("2024-12-25")
print(date2.format())

print(f"2024年是闰年：{Date.is_leap_year(2024)}")
print(f"2023年是闰年：{Date.is_leap_year(2023)}")


# ========== 练习8：综合练习 - 购物车系统 ==========
print("\n=== 练习8：购物车系统 ===")
"""
题目：实现一个简单的购物车系统
要求：
1. 创建 CartItem 类表示购物车条目（商品名、价格、数量）
2. 创建 ShoppingCart 类表示购物车
3. ShoppingCart 包含方法：
   - add_item(name, price, quantity): 添加商品
   - remove_item(name): 移除商品
   - get_total(): 计算总价
   - get_item_count(): 获取商品种类数
   - clear(): 清空购物车
4. 实现 __str__ 显示购物车内容
"""


class CartItem:
    """购物车条目"""

    def __init__(self, name, price, quantity):
        """
        初始化购物车条目

        Args:
            name: 商品名
            price: 单价
            quantity: 数量
        """
        # TODO: 在这里实现你的代码
        pass

    def get_subtotal(self):
        """
        计算小计

        Returns:
            float: 该商品的总价
        """
        # TODO: 在这里实现你的代码
        pass

    def __str__(self):
        """字符串表示"""
        # TODO: 在这里实现你的代码
        pass


class ShoppingCart:
    """购物车类"""

    def __init__(self):
        """初始化购物车"""
        # TODO: 在这里实现你的代码
        # 提示：使用字典存储商品，键为商品名，值为CartItem对象
        pass

    def add_item(self, name, price, quantity):
        """
        添加商品

        Args:
            name: 商品名
            price: 单价
            quantity: 数量
        """
        # TODO: 在这里实现你的代码
        pass

    def remove_item(self, name):
        """
        移除商品

        Args:
            name: 商品名

        Returns:
            bool: 是否移除成功
        """
        # TODO: 在这里实现你的代码
        pass

    def get_total(self):
        """
        计算总价

        Returns:
            float: 购物车总价
        """
        # TODO: 在这里实现你的代码
        pass

    def get_item_count(self):
        """
        获取商品种类数

        Returns:
            int: 商品种类数
        """
        # TODO: 在这里实现你的代码
        pass

    def clear(self):
        """清空购物车"""
        # TODO: 在这里实现你的代码
        pass

    def __str__(self):
        """字符串表示"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
cart = ShoppingCart()
cart.add_item("笔记本电脑", 5999, 1)
cart.add_item("鼠标", 99, 2)
cart.add_item("键盘", 299, 1)

print("购物车内容：")
print(cart)
print(f"总价：¥{cart.get_total():.2f}")
print(f"商品种类：{cart.get_item_count()}")

cart.remove_item("鼠标")
print("\n移除鼠标后：")
print(cart)
print(f"总价：¥{cart.get_total():.2f}")


print("\n面向对象入门练习完成！")
print("\n提示：完成所有TODO部分后，运行此文件查看结果")
