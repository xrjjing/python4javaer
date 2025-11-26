#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 快速上手与基本语法示例
演示：缩进、注释、输入输出、基本运算
"""

# 这是单行注释
# input() 函数获取用户输入，返回字符串
name = input("请输入你的名字：")

# print() 函数输出内容到控制台
print("你好，", name)
print(f"欢迎学习 Python！")

# 基本算术运算
print("\n=== 基本运算 ===")
num1 = 10
num2 = 3
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")

# Python 的缩进很重要（用4个空格表示代码块）
if True:
    print("\n这是 if 语句内的代码块")
    print("缩进必须保持一致")

# 多行字符串
multiline = """
这是一个
多行字符串
可以包含换行
"""
print(multiline)
