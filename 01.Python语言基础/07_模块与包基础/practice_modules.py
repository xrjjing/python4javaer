#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：模块与包基础
"""

# 练习1：使用标准库模块
print("=== 练习1：标准库模块应用 ===")
import math
import random
import datetime

# 计算圆的面积和周长
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius
print(f"半径为{radius}的圆：")
print(f"  面积：{area:.2f}")
print(f"  周长：{circumference:.2f}")

# 生成随机密码
import string
def generate_password(length=8):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))

print(f"\n随机密码：{generate_password(12)}")

# 日期计算
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
next_week = today + datetime.timedelta(weeks=1)
print(f"\n今天：{today}")
print(f"明天：{tomorrow}")
print(f"下周：{next_week}")

# 练习2：创建自定义模块
print("\n=== 练习2：创建自定义模块 ===")
import os

# 创建 string_utils.py 模块
string_utils_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字符串工具模块"""

def reverse(text):
    """反转字符串"""
    return text[::-1]

def is_palindrome(text):
    """判断是否为回文"""
    text = text.lower().replace(" ", "")
    return text == text[::-1]

def count_words(text):
    """统计单词数"""
    return len(text.split())

def capitalize_words(text):
    """首字母大写"""
    return ' '.join(word.capitalize() for word in text.split())

if __name__ == "__main__":
    print("字符串工具模块测试")
    print(reverse("Hello"))
    print(is_palindrome("A man a plan a canal Panama"))
'''

with open("string_utils.py", "w", encoding="utf-8") as f:
    f.write(string_utils_content)

try:
    import string_utils

    test_text = "hello world"
    print(f"原文本：{test_text}")
    print(f"反转：{string_utils.reverse(test_text)}")
    print(f"单词数：{string_utils.count_words(test_text)}")
    print(f"首字母大写：{string_utils.capitalize_words(test_text)}")

    palindrome = "A man a plan a canal Panama"
    print(f"\n'{palindrome}' 是回文吗？{string_utils.is_palindrome(palindrome)}")

finally:
    if os.path.exists("string_utils.py"):
        os.remove("string_utils.py")
    if os.path.exists("__pycache__"):
        import shutil
        shutil.rmtree("__pycache__")

# 练习3：创建数学工具模块
print("\n=== 练习3：数学工具模块 ===")

math_utils_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数学工具模块"""

def factorial(n):
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """生成斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def is_prime(n):
    """判断是否为素数"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """计算最小公倍数"""
    return abs(a * b) // gcd(a, b)
'''

with open("math_utils.py", "w", encoding="utf-8") as f:
    f.write(math_utils_content)

try:
    import math_utils

    print(f"5的阶乘：{math_utils.factorial(5)}")
    print(f"前10项斐波那契数列：{math_utils.fibonacci(10)}")
    print(f"17是素数吗？{math_utils.is_prime(17)}")
    print(f"18是素数吗？{math_utils.is_prime(18)}")
    print(f"12和18的最大公约数：{math_utils.gcd(12, 18)}")
    print(f"12和18的最小公倍数：{math_utils.lcm(12, 18)}")

finally:
    if os.path.exists("math_utils.py"):
        os.remove("math_utils.py")
    if os.path.exists("__pycache__"):
        import shutil
        shutil.rmtree("__pycache__")

# 练习4：使用 collections 模块
print("\n=== 练习4：collections 模块 ===")
from collections import Counter, defaultdict, namedtuple

# Counter - 计数器
text = "hello world hello python"
word_count = Counter(text.split())
print(f"单词频次：{word_count}")
print(f"最常见的2个单词：{word_count.most_common(2)}")

# defaultdict - 默认字典
students = [
    ("张三", "数学"),
    ("李四", "语文"),
    ("王五", "数学"),
    ("赵六", "英语"),
    ("张三", "语文"),
]

subject_students = defaultdict(list)
for student, subject in students:
    subject_students[subject].append(student)

print(f"\n按科目分组：")
for subject, names in subject_students.items():
    print(f"  {subject}：{', '.join(names)}")

# namedtuple - 命名元组
Point = namedtuple('Point', ['x', 'y'])
p1 = Point(3, 4)
print(f"\n点坐标：x={p1.x}, y={p1.y}")
print(f"距离原点：{math.sqrt(p1.x**2 + p1.y**2):.2f}")

# 练习5：使用 itertools 模块
print("\n=== 练习5：itertools 模块 ===")
from itertools import combinations, permutations, product

# 组合
items = ['A', 'B', 'C']
print(f"从{items}中选2个的组合：")
for combo in combinations(items, 2):
    print(f"  {combo}")

# 排列
print(f"\n从{items}中选2个的排列：")
for perm in permutations(items, 2):
    print(f"  {perm}")

# 笛卡尔积
colors = ['红', '蓝']
sizes = ['大', '小']
print(f"\n颜色和尺寸的笛卡尔积：")
for item in product(colors, sizes):
    print(f"  {item}")

# 练习6：文件操作模块
print("\n=== 练习6：文件操作 ===")
import os
import shutil
import tempfile

# 创建临时目录
temp_dir = tempfile.mkdtemp()
print(f"临时目录：{temp_dir}")

try:
    # 创建文件
    file_path = os.path.join(temp_dir, "test.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Hello, Python!")

    print(f"文件是否存在：{os.path.exists(file_path)}")
    print(f"文件大小：{os.path.getsize(file_path)} 字节")

    # 复制文件
    copy_path = os.path.join(temp_dir, "test_copy.txt")
    shutil.copy(file_path, copy_path)
    print(f"复制文件成功")

    # 列出目录内容
    print(f"目录内容：{os.listdir(temp_dir)}")

finally:
    # 清理临时目录
    shutil.rmtree(temp_dir)
    print(f"已清理临时目录")

# 练习7：JSON 和 CSV 处理
print("\n=== 练习7：JSON 和 CSV 处理 ===")
import json
import csv

# JSON 处理
data = {
    "students": [
        {"name": "张三", "age": 20, "score": 85},
        {"name": "李四", "age": 21, "score": 92},
        {"name": "王五", "age": 20, "score": 78},
    ]
}

json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(f"JSON 字符串：\n{json_str}")

# CSV 处理
csv_file = "students.csv"
try:
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "score"])
        writer.writeheader()
        writer.writerows(data["students"])

    print(f"\n写入 CSV 文件成功")

    # 读取 CSV
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(f"读取 CSV 内容：")
        for row in reader:
            print(f"  {row['name']}：{row['age']}岁，成绩{row['score']}")

finally:
    if os.path.exists(csv_file):
        os.remove(csv_file)

# 练习8：正则表达式模块
print("\n=== 练习8：正则表达式 ===")
import re

text = "联系方式：13800138000，邮箱：user@example.com"

# 查找手机号
phone_pattern = r'1[3-9]\d{9}'
phones = re.findall(phone_pattern, text)
print(f"手机号：{phones}")

# 查找邮箱
email_pattern = r'\w+@\w+\.\w+'
emails = re.findall(email_pattern, text)
print(f"邮箱：{emails}")

# 替换
masked_text = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', text)
print(f"脱敏后：{masked_text}")

print("\n模块练习完成！")
