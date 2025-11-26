#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
条件判断与分支示例
演示：if/elif/else、布尔表达式、常见陷阱
"""

# 1. 基本 if 语句
print("=== 基本 if 语句 ===")
age = 18

if age >= 18:
    print("成年人，可以投票")
    print("需要承担法律责任")

# 2. if-else 语句
print("\n=== if-else 语句 ===")
score = 85

if score >= 60:
    print("考试通过！")
else:
    print("考试未通过，需要补考")

# 3. if-elif-else 多分支
print("\n=== 多分支判断 ===")
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数：{score}，等级：{grade}")

# 4. 嵌套条件
print("\n=== 嵌套条件 ===")
age = 25
has_license = True

if age >= 18:
    print("已成年")
    if has_license:
        print("有驾照，可以开车")
    else:
        print("没有驾照，需要考取")
else:
    print("未成年，无法考取驾照")

# 5. 布尔表达式
print("\n=== 布尔表达式 ===")
x = 5
y = 10
z = 15

print(f"x = {x}, y = {y}, z = {z}")
print(f"x < y and y < z: {x < y and y < z}")  # True
print(f"x > y or y < z: {x > y or y < z}")    # True
print(f"not x == y: {not x == y}")            # True

# 6. 常见陷阱：空字符串和空列表的真值
print("\n=== 真值测试陷阱 ===")
empty_str = ""
empty_list = []
empty_dict = {}
zero = 0
none_value = None

print(f"空字符串 '': {bool(empty_str)}")
print(f"空列表 []: {bool(empty_list)}")
print(f"空字典 {{}}: {bool(empty_dict)}")
print(f"数字 0: {bool(zero)}")
print(f"None: {bool(none_value)}")

# 非空的值
text = "hello"
nums = [1, 2, 3]
print(f"字符串 'hello': {bool(text)}")
print(f"列表 [1, 2, 3]: {bool(nums)}")

# 7. 使用布尔值进行条件判断
print("\n=== 布尔值判断 ===")
items = []

# 检查列表是否为空（两种方式）
if len(items) == 0:
    print("列表为空（方式1）")

if not items:
    print("列表为空（方式2，推荐）")

# 8. 三元运算符（条件表达式）
print("\n=== 三元运算符 ===")
age = 20
status = "成年人" if age >= 18 else "未成年人"
print(f"年龄：{age}，状态：{status}")

# 9. 多个条件的组合
print("\n=== 条件组合 ===")
temperature = 25
is_sunny = True
is_weekend = False

if temperature > 20 and is_sunny and not is_weekend:
    print("天气很好，适合外出")
elif temperature > 20 and is_sunny and is_weekend:
    print("周末好天气，可以旅游")
elif temperature <= 0 or (is_sunny and temperature < 10):
    print("天气较冷，注意保暖")
else:
    print("天气一般")

# 10. in 操作符检查成员关系
print("\n=== 成员检查 ===")
fruits = ["苹果", "香蕉", "橙子"]
fruit = "香蕉"

if fruit in fruits:
    print(f"{fruit} 在水果列表中")
else:
    print(f"{fruit} 不在水果列表中")

# 检查用户名
valid_usernames = ["admin", "user1", "user2"]
username = "user3"

if username in valid_usernames:
    print("用户名有效")
else:
    print("用户名无效")

# 11. pass 语句（占位符）
print("\n=== pass 占位符 ===")
score = 95

if score >= 90:
    pass  # 以后再实现优秀学生的处理逻辑
elif score >= 60:
    print("考试通过")
else:
    print("考试未通过")
