#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正则表达式示例
演示：re模块、常用模式、匹配、查找、替换、分组
"""

import re

# 1. 基本匹配
print("=== 基本匹配 ===")
text = "Hello, my phone is 13800138000"

# 查找手机号
pattern = r'1[3-9]\d{9}'
match = re.search(pattern, text)
if match:
    print(f"找到手机号：{match.group()}")

# 2. 常用元字符
print("\n=== 常用元字符 ===")
# . 匹配任意字符（除换行符）
# ^ 匹配字符串开头
# $ 匹配字符串结尾
# * 匹配0次或多次
# + 匹配1次或多次
# ? 匹配0次或1次
# {n} 匹配n次
# {n,} 匹配至少n次
# {n,m} 匹配n到m次

text = "abc123def456"
print(f"文本：{text}")
print(f"\\d+ 匹配数字：{re.findall(r'\d+', text)}")
print(f"\\w+ 匹配单词：{re.findall(r'\w+', text)}")
print(f"[a-z]+ 匹配小写字母：{re.findall(r'[a-z]+', text)}")

# 3. 字符类
print("\n=== 字符类 ===")
text = "Email: user@example.com, Phone: 13800138000"

# \d 数字 [0-9]
# \D 非数字
# \w 单词字符 [a-zA-Z0-9_]
# \W 非单词字符
# \s 空白字符
# \S 非空白字符

print(f"\\d+ 数字：{re.findall(r'\d+', text)}")
print(f"\\w+ 单词：{re.findall(r'\w+', text)}")

# 4. 分组和捕获
print("\n=== 分组和捕获 ===")
text = "张三的手机号是13800138000，李四的手机号是13900139000"

# 使用括号分组
pattern = r'(\w+)的手机号是(\d{11})'
matches = re.findall(pattern, text)
for name, phone in matches:
    print(f"{name}：{phone}")

# 5. 命名分组
print("\n=== 命名分组 ===")
text = "2025-01-15"
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.search(pattern, text)
if match:
    print(f"年：{match.group('year')}")
    print(f"月：{match.group('month')}")
    print(f"日：{match.group('day')}")

# 6. 邮箱验证
print("\n=== 邮箱验证 ===")
emails = [
    "user@example.com",
    "test.user@company.co.uk",
    "invalid@",
    "@invalid.com",
    "user@domain",
]

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
for email in emails:
    is_valid = bool(re.match(email_pattern, email))
    print(f"{email:30s} {'✓' if is_valid else '✗'}")

# 7. 手机号验证
print("\n=== 手机号验证 ===")
phones = [
    "13800138000",
    "15912345678",
    "12345678901",
    "138001380",
    "1380013800a",
]

phone_pattern = r'^1[3-9]\d{9}$'
for phone in phones:
    is_valid = bool(re.match(phone_pattern, phone))
    print(f"{phone:15s} {'✓' if is_valid else '✗'}")

# 8. URL提取
print("\n=== URL提取 ===")
text = """
访问我们的网站：https://www.example.com
或者：http://blog.example.com/post/123
FTP地址：ftp://files.example.com
"""

url_pattern = r'https?://[^\s]+'
urls = re.findall(url_pattern, text)
print("找到的URL：")
for url in urls:
    print(f"  {url}")

# 9. 替换操作
print("\n=== 替换操作 ===")
text = "联系电话：13800138000，备用电话：13900139000"

# 简单替换
masked = re.sub(r'\d{11}', '***********', text)
print(f"完全隐藏：{masked}")

# 部分隐藏
masked = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', text)
print(f"部分隐藏：{masked}")

# 10. 分割字符串
print("\n=== 分割字符串 ===")
text = "apple,banana;orange|grape"
parts = re.split(r'[,;|]', text)
print(f"分割结果：{parts}")

# 11. 贪婪与非贪婪匹配
print("\n=== 贪婪与非贪婪 ===")
html = "<div>内容1</div><div>内容2</div>"

# 贪婪匹配（默认）
greedy = re.findall(r'<div>.*</div>', html)
print(f"贪婪匹配：{greedy}")

# 非贪婪匹配
non_greedy = re.findall(r'<div>.*?</div>', html)
print(f"非贪婪匹配：{non_greedy}")

# 12. 编译正则表达式
print("\n=== 编译正则表达式 ===")
# 频繁使用的模式应该编译
phone_regex = re.compile(r'1[3-9]\d{9}')

texts = [
    "我的手机号是13800138000",
    "联系方式：15912345678",
    "没有手机号",
]

for text in texts:
    match = phone_regex.search(text)
    if match:
        print(f"{text} → {match.group()}")
    else:
        print(f"{text} → 未找到")

# 13. 多行模式
print("\n=== 多行模式 ===")
text = """第一行
第二行
第三行"""

# 默认 ^ 和 $ 只匹配整个字符串的开头和结尾
# MULTILINE 模式下，^ 和 $ 匹配每行的开头和结尾
lines = re.findall(r'^第.*', text, re.MULTILINE)
print(f"匹配的行：{lines}")

# 14. 忽略大小写
print("\n=== 忽略大小写 ===")
text = "Python is great, PYTHON is awesome"
matches = re.findall(r'python', text, re.IGNORECASE)
print(f"匹配次数：{len(matches)}")

# 15. 实用示例：日志解析
print("\n=== 日志解析 ===")
log_lines = [
    "2025-01-15 10:30:45 [INFO] 用户登录成功",
    "2025-01-15 10:31:20 [ERROR] 数据库连接失败",
    "2025-01-15 10:32:10 [WARNING] 内存使用率过高",
]

log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)'
for line in log_lines:
    match = re.match(log_pattern, line)
    if match:
        timestamp, level, message = match.groups()
        print(f"时间：{timestamp}, 级别：{level}, 消息：{message}")

# 16. 实用示例：提取HTML标签内容
print("\n=== 提取HTML内容 ===")
html = "<h1>标题</h1><p>段落1</p><p>段落2</p>"
paragraphs = re.findall(r'<p>(.*?)</p>', html)
print(f"段落内容：{paragraphs}")

# 17. 实用示例：身份证号验证
print("\n=== 身份证号验证 ===")
id_cards = [
    "110101199001011234",
    "12345678901234567",
    "11010119900101123X",
]

id_pattern = r'^\d{17}[\dXx]$'
for id_card in id_cards:
    is_valid = bool(re.match(id_pattern, id_card))
    print(f"{id_card} {'✓' if is_valid else '✗'}")

print("\n正则表达式演示完成！")
