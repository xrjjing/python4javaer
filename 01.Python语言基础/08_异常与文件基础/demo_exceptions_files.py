#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常与文件基础示例
演示：try/except/else/finally、raise、文件操作、with语句
"""

# 1. 基本异常处理
print("=== 基本异常处理 ===")
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"错误：{e}")
    print("除数不能为零")

# 2. 多种异常类型
print("\n=== 多种异常类型 ===")
try:
    num = int("abc")
    result = 10 / 0
except ValueError as e:
    print(f"值错误：{e}")
except ZeroDivisionError as e:
    print(f"除零错误：{e}")

# 3. 使用else和finally
print("\n=== else和finally ===")
try:
    num = int("123")
    result = 100 / num
except ValueError as e:
    print(f"转换错误：{e}")
except ZeroDivisionError as e:
    print(f"除零错误：{e}")
else:
    print(f"计算成功，结果：{result}")
finally:
    print("无论是否异常，都会执行finally")

# 4. 主动抛出异常
print("\n=== 主动抛出异常 ===")
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不能超过150")
    return age

try:
    check_age(-5)
except ValueError as e:
    print(f"异常：{e}")

# 5. 自定义异常
print("\n=== 自定义异常 ===")
class InsufficientBalanceError(Exception):
    """余额不足异常"""
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(f"余额不足，当前余额：{balance}，需要：{amount}")
    return balance - amount

try:
    new_balance = withdraw(100, 150)
except InsufficientBalanceError as e:
    print(f"取款失败：{e}")

# 6. 文件操作基础
print("\n=== 文件操作 ===")
import os

# 写入文件
content = "Hello, Python!\n这是第二行"
file_path = "test_file.txt"

try:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"写入文件成功：{file_path}")

    # 读取文件
    with open(file_path, "r", encoding="utf-8") as f:
        read_content = f.read()
    print(f"读取内容：{read_content}")

finally:
    # 清理文件
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"已删除文件：{file_path}")

# 7. 逐行读取大文件
print("\n=== 逐行读取 ===")
content_lines = ["第1行", "第2行", "第3行", "第4行", "第5行"]
file_path = "lines.txt"

with open(file_path, "w", encoding="utf-8") as f:
    for line in content_lines:
        f.write(line + "\n")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        line_number = 1
        for line in f:
            print(f"第{line_number}行：{line.strip()}")
            line_number += 1
finally:
    os.remove(file_path)

# 8. JSON文件操作
print("\n=== JSON文件操作 ===")
import json

data = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "Java", "SQL"],
    "is_employed": True
}

json_file = "data.json"

try:
    # 写入JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("写入JSON文件成功")

    # 读取JSON
    with open(json_file, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(f"读取数据：{loaded_data}")
    print(f"姓名：{loaded_data['name']}")
    print(f"技能：{', '.join(loaded_data['skills'])}")
finally:
    os.remove(json_file)

# 9. CSV文件操作
print("\n=== CSV文件操作 ===")
import csv

csv_file = "employees.csv"

try:
    # 写入CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["姓名", "部门", "薪资"])
        writer.writerow(["张三", "技术部", 12000])
        writer.writerow(["李四", "销售部", 15000])
        writer.writerow(["王五", "财务部", 10000])
    print("写入CSV文件成功")

    # 读取CSV
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("员工信息：")
        for row in reader:
            print(f"  {row['姓名']}：{row['部门']}，薪资{row['薪资']}")
finally:
    os.remove(csv_file)

# 10. 上下文管理器（with语句）
print("\n=== 上下文管理器 ===")
class FileHandler:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        print("文件已关闭")
        return False

file_path = "demo.txt"

try:
    with FileHandler(file_path, "w") as f:
        f.write("Hello, Context Manager!")
    print("写入成功")
finally:
    if os.path.exists(file_path):
        os.remove(file_path)

# 11. 资源管理和异常安全
print("\n=== 资源管理 ===")
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"除零错误：{e}")
        return None
    finally:
        print("除法计算完成")

result1 = safe_divide(10, 2)
result2 = safe_divide(10, 0)

print(f"结果1：{result1}")
print(f"结果2：{result2}")
