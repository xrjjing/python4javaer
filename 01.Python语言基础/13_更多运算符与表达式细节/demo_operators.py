#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更多运算符与表达式细节示例
演示：成员运算符、身份运算符、运算符优先级、pass语句、海象运算符
"""

# 1. 成员运算符 in / not in
print("=== 成员运算符 ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"水果列表：{fruits}")
print(f"'苹果' in fruits: {'苹果' in fruits}")
print(f"'葡萄' in fruits: {'葡萄' in fruits}")
print(f"'葡萄' not in fruits: {'葡萄' not in fruits}")

# 字符串成员检查
text = "Hello, Python!"
print(f"\n文本：'{text}'")
print(f"'Python' in text: {'Python' in text}")
print(f"'Java' not in text: {'Java' not in text}")

# 字典成员检查（检查键）
person = {"name": "张三", "age": 25}
print(f"\n字典：{person}")
print(f"'name' in person: {'name' in person}")
print(f"'email' in person: {'email' in person}")

# 2. 身份运算符 is / is not
print("\n=== 身份运算符 ===")
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a = {a}, id(a) = {id(a)}")
print(f"b = {b}, id(b) = {id(b)}")
print(f"c = a, id(c) = {id(c)}")

print(f"\na == b: {a == b}")  # 值相等
print(f"a is b: {a is b}")    # 不是同一个对象
print(f"a is c: {a is c}")    # 是同一个对象

# None 的比较
x = None
print(f"\nx is None: {x is None}")  # 推荐
print(f"x == None: {x == None}")    # 不推荐

# 小整数缓存
num1 = 256
num2 = 256
print(f"\nnum1 = 256, num2 = 256")
print(f"num1 is num2: {num1 is num2}")  # True（小整数缓存）

num3 = 257
num4 = 257
print(f"\nnum3 = 257, num4 = 257")
print(f"num3 is num4: {num3 is num4}")  # False（超出缓存范围）

# 3. 运算符优先级
print("\n=== 运算符优先级 ===")
# 从高到低：
# 1. 括号 ()
# 2. 乘方 **
# 3. 正负号 +x, -x
# 4. 乘除 *, /, //, %
# 5. 加减 +, -
# 6. 比较 <, <=, >, >=, ==, !=
# 7. 逻辑非 not
# 8. 逻辑与 and
# 9. 逻辑或 or

result1 = 2 + 3 * 4
result2 = (2 + 3) * 4
result3 = 2 ** 3 ** 2  # 右结合
result4 = 10 + 5 * 2 - 3

print(f"2 + 3 * 4 = {result1}")
print(f"(2 + 3) * 4 = {result2}")
print(f"2 ** 3 ** 2 = {result3}")  # 2 ** (3 ** 2) = 512
print(f"10 + 5 * 2 - 3 = {result4}")

# 逻辑运算符优先级
x = 5
result5 = x > 3 and x < 10
result6 = x > 3 or x < 0 and x > 10
print(f"\nx = {x}")
print(f"x > 3 and x < 10: {result5}")
print(f"x > 3 or x < 0 and x > 10: {result6}")

# 4. pass 语句
print("\n=== pass 语句 ===")
# 空函数
def empty_function():
    pass

# 空类
class EmptyClass:
    pass

# 条件分支占位
score = 95
if score >= 90:
    pass  # TODO: 实现优秀学生奖励逻辑
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 循环占位
for i in range(5):
    if i == 2:
        pass  # TODO: 特殊处理
    else:
        print(i)

# 5. 海象运算符 := (Python 3.8+)
print("\n=== 海象运算符 := ===")
# 在表达式中赋值
numbers = [1, 2, 3, 4, 5]
if (n := len(numbers)) > 3:
    print(f"列表长度 {n} 大于 3")

# 在 while 循环中使用
print("\n输入处理（输入'quit'退出）：")
# while (line := input("请输入：")) != "quit":
#     print(f"你输入了：{line}")

# 在列表推导式中使用
data = [1, 2, 3, 4, 5]
filtered = [y for x in data if (y := x * 2) > 5]
print(f"过滤结果：{filtered}")

# 6. 位运算符
print("\n=== 位运算符 ===")
a = 60  # 0011 1100
b = 13  # 0000 1101

print(f"a = {a} (二进制：{bin(a)})")
print(f"b = {b} (二进制：{bin(b)})")
print(f"a & b = {a & b} (按位与)")
print(f"a | b = {a | b} (按位或)")
print(f"a ^ b = {a ^ b} (按位异或)")
print(f"~a = {~a} (按位取反)")
print(f"a << 2 = {a << 2} (左移)")
print(f"a >> 2 = {a >> 2} (右移)")

# 7. 三元运算符（条件表达式）
print("\n=== 三元运算符 ===")
age = 20
status = "成年人" if age >= 18 else "未成年人"
print(f"年龄 {age}，状态：{status}")

# 嵌套三元运算符
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D"
print(f"分数 {score}，等级：{grade}")

# 8. 链式比较
print("\n=== 链式比较 ===")
x = 5
print(f"x = {x}")
print(f"1 < x < 10: {1 < x < 10}")
print(f"1 < x <= 5: {1 < x <= 5}")
print(f"x == 5 == 5: {x == 5 == 5}")

# 9. 短路求值
print("\n=== 短路求值 ===")
def func1():
    print("func1 被调用")
    return True

def func2():
    print("func2 被调用")
    return False

print("测试 and 短路：")
result = func2() and func1()  # func1 不会被调用

print("\n测试 or 短路：")
result = func1() or func2()  # func2 不会被调用

# 10. 解包运算符
print("\n=== 解包运算符 ===")
# * 解包列表
numbers = [1, 2, 3]
more_numbers = [*numbers, 4, 5, 6]
print(f"解包列表：{more_numbers}")

# ** 解包字典
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = {**dict1, **dict2}
print(f"解包字典：{merged}")

# 函数参数解包
def add(a, b, c):
    return a + b + c

args = [1, 2, 3]
result = add(*args)
print(f"参数解包：add(*{args}) = {result}")

kwargs = {"a": 1, "b": 2, "c": 3}
result = add(**kwargs)
print(f"关键字参数解包：add(**{kwargs}) = {result}")

# 11. 扩展解包
print("\n=== 扩展解包 ===")
# 列表解包
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# 忽略某些值
a, _, c = [1, 2, 3]
print(f"a={a}, c={c}")

# 12. 运算符重载
print("\n=== 运算符重载 ===")
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """重载 + 运算符"""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """重载 * 运算符"""
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
v4 = v1 * 3

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v3}")
print(f"v1 * 3 = {v4}")

# 13. 比较运算符重载
print("\n=== 比较运算符重载 ===")
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        """重载 == 运算符"""
        return self.age == other.age

    def __lt__(self, other):
        """重载 < 运算符"""
        return self.age < other.age

    def __str__(self):
        return f"{self.name}({self.age}岁)"

p1 = Person("张三", 25)
p2 = Person("李四", 30)
p3 = Person("王五", 25)

print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"p3 = {p3}")
print(f"p1 == p3: {p1 == p3}")
print(f"p1 < p2: {p1 < p2}")

# 排序
people = [p2, p1, p3]
sorted_people = sorted(people)
print(f"排序后：{[str(p) for p in sorted_people]}")

# 14. 布尔运算的返回值
print("\n=== 布尔运算的返回值 ===")
# and 返回第一个假值或最后一个值
print(f"1 and 2: {1 and 2}")  # 2
print(f"0 and 2: {0 and 2}")  # 0
print(f"[] and 'hello': {[] and 'hello'}")  # []

# or 返回第一个真值或最后一个值
print(f"1 or 2: {1 or 2}")  # 1
print(f"0 or 2: {0 or 2}")  # 2
print(f"[] or 'hello': {[] or 'hello'}")  # 'hello'

# 实用技巧：提供默认值
name = ""
display_name = name or "匿名用户"
print(f"显示名称：{display_name}")

print("\n运算符与表达式演示完成！")
