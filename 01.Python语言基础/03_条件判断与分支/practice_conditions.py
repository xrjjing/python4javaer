#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：条件判断与分支
"""

# 练习1：成绩等级判定
print("=== 练习1：成绩等级判定 ===")
score = float(input("请输入成绩（0-100）："))

if score > 100 or score < 0:
    print("成绩输入错误！")
elif score >= 90:
    print(f"成绩：{score}，等级：A（优秀）")
elif score >= 80:
    print(f"成绩：{score}，等级：B（良好）")
elif score >= 70:
    print(f"成绩：{score}，等级：C（中等）")
elif score >= 60:
    print(f"成绩：{score}，等级：D（及格）")
else:
    print(f"成绩：{score}，等级：F（不及格）")

# 练习2：BMI计算与健康建议
print("\n=== 练习2：BMI计算与健康建议 ===")
height = float(input("请输入身高（米）："))
weight = float(input("请输入体重（公斤）："))

# BMI = 体重(kg) / 身高(m)^2
bmi = weight / (height ** 2)

print(f"\n身高：{height}m，体重：{weight}kg")
print(f"BMI：{bmi:.2f}")

if bmi < 18.5:
    print("体重过轻，建议增加营养")
elif 18.5 <= bmi < 24:
    print("体重正常，保持良好")
elif 24 <= bmi < 28:
    print("体重过重，建议运动减肥")
else:
    print("肥胖，建议咨询医生制定减肥计划")

# 练习3：简单登录验证
print("\n=== 练习3：登录验证 ===")
correct_username = "admin"
correct_password = "123456"

username = input("请输入用户名：")
password = input("请输入密码：")

if username == correct_username and password == correct_password:
    print("登录成功！")
elif username == correct_username:
    print("密码错误！")
elif password == correct_password:
    print("用户名错误！")
else:
    print("用户名和密码都错误！")

# 练习4：简单计算器
print("\n=== 练习4：简单计算器 ===")
num1 = float(input("请输入第一个数字："))
operator = input("请输入运算符（+、-、*、/）：")
num2 = float(input("请输入第二个数字："))

if operator == "+":
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
elif operator == "-":
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
elif operator == "*":
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
elif operator == "/":
    if num2 != 0:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
    else:
        print("错误：除数不能为0！")
else:
    print("无效的运算符！")

# 练习5：年份与闰年判断
print("\n=== 练习5：闰年判断 ===")
year = int(input("请输入年份："))

# 闰年规则：能被4整除但不能被100整除，或能被400整除
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} 年是闰年")
else:
    print(f"{year} 年是平年")

# 练习6：交通灯判断
print("\n=== 练习6：交通灯判断 ===")
light = input("请输入灯的颜色（红/黄/绿）：")

if light == "红":
    print("红灯停")
elif light == "黄":
    print("黄灯等一等")
elif light == "绿":
    print("绿灯行")
else:
    print("无效的灯色")

# 练习7：折扣计算
print("\n=== 练习7：折扣计算 ===")
original_price = float(input("请输入商品原价："))
member_level = input("请输入会员等级（普通/银卡/金卡/钻石）：")

if member_level == "普通":
    discount = 0
    final_price = original_price
elif member_level == "银卡":
    discount = 0.05
    final_price = original_price * 0.95
elif member_level == "金卡":
    discount = 0.10
    final_price = original_price * 0.90
elif member_level == "钻石":
    discount = 0.15
    final_price = original_price * 0.85
else:
    print("无效的会员等级！")
    discount = 0
    final_price = original_price

if discount > 0:
    print(f"原价：{original_price}元")
    print(f"会员等级：{member_level}")
    print(f"折扣：{discount*100}%")
    print(f"实付：{final_price}元")
else:
    print(f"原价：{original_price}元")
    print("不是会员，无折扣")

# 练习8：真值判断总结
print("\n=== 练习8：真值判断 ===")
print("以下值的布尔值为 False：")
print(f"  0: {bool(0)}")
print(f"  0.0: {bool(0.0)}")
print(f"  '': {bool('')}")
print(f"  []: {bool([])}")
print(f"  {{}}: {bool({})}")
print(f"  None: {bool(None)}")

print("\n以下值的布尔值为 True：")
print(f"  非0数字: {bool(1)}")
print(f"  非空字符串: {bool('hello')}")
print(f"  非空列表: {bool([1, 2])}")
print(f"  非空字典: {bool({'a': 1})}")
