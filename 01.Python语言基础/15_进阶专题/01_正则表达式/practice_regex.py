#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正则表达式进阶练习
练习：基础匹配、分组、命名分组、替换、日志解析
"""

import re


print("=== 练习1：基础匹配与搜索 ===")
"""
题目：完成几个常见模式的正则表达式
要求：
1. 匹配 3 位或 4 位数字（例如 404、2024）
2. 匹配邮箱地址（简单版本：username@domain.com）
3. 匹配日期字符串：YYYY-MM-DD（例如 2024-01-31）
"""

# TODO: 在这里补全正则模式（使用原始字符串 r""）
# pattern_digits = r"..."
# pattern_email = r"..."
# pattern_date = r"..."

# 测试代码（完成后可取消注释）
# tests = ["404", "2024", "12a4"]
# for t in tests:
#     print(t, "匹配数字：", bool(re.fullmatch(pattern_digits, t)))
#
# emails = ["user@example.com", "abc@x.cn", "bad@@example.com"]
# for e in emails:
#     print(e, "是邮箱：", bool(re.fullmatch(pattern_email, e)))
#
# dates = ["2024-01-31", "2024-13-01", "2024-01-1"]
# for d in dates:
#     print(d, "是日期格式：", bool(re.fullmatch(pattern_date, d)))


print("\n=== 练习2：日志行解析（命名分组） ===")
"""
题目：解析简单日志行
日志格式示例：
    [2024-01-01 10:00:00] INFO user=tom action=login

要求：
1. 使用命名分组提取：
   - 时间戳 timestamp
   - 日志级别 level
   - 用户 user
   - 动作 action
2. 封装函数 parse_log_line(line: str) -> dict | None
   - 匹配成功返回字典
   - 匹配失败返回 None
"""


def parse_log_line(line: str) -> dict | None:
    """解析日志行，返回包含四个字段的字典或 None。"""
    # TODO: 在这里编写正则并完成解析逻辑
    # 提示：可以先 compile，再调用 match()
    # pattern = re.compile(r"...")
    # m = pattern.match(line)
    # if not m: return None
    # return m.groupdict()
    raise NotImplementedError("请在这里实现日志解析逻辑")


# 测试代码（完成后可取消注释）
# sample_lines = [
#     "[2024-01-01 10:00:00] INFO user=tom action=login",
#     "[2024-01-01 10:05:00] ERROR user=alice action=pay",
#     "bad line",
# ]
# for line in sample_lines:
#     print(line)
#     print("解析结果：", parse_log_line(line))


print("\n=== 练习3：文本清洗与替换 ===")
"""
题目：使用 re.sub 完成以下任务
1. 将字符串中连续多个空格压缩成一个空格
   例如："hello   world   python" -> "hello world python"
2. 将文本中的手机号脱敏：
   - 假设手机号格式为 11 位数字，如 13812345678
   - 显示前三位和后四位，中间用 * 代替：138****5678
"""


def normalize_spaces(text: str) -> str:
    """将连续空格压缩为一个空格。"""
    # TODO: 使用 re.sub 实现
    raise NotImplementedError


def mask_phone(text: str) -> str:
    """将文本中出现的 11 位手机号脱敏处理。"""
    # TODO: 使用 re.sub + 分组引用实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(normalize_spaces("hello   world   python"))
# print(mask_phone("我的电话是13812345678，请保密。"))


print("\n=== 练习4：多行文本处理 ===")
"""
题目：从多行配置文本中提取 key=value 配置
示例文本：
    # app config
    host=localhost
    port=8080
    debug=true

要求：
1. 忽略以 # 开头的注释行和空行
2. 提取形如 key=value 的配置，去掉两侧空白
3. 返回一个字典，例如：{"host": "localhost", "port": "8080", "debug": "true"}
"""


def parse_simple_config(text: str) -> dict:
    """解析简单配置文本为字典。"""
    # TODO: 使用 re.MULTILINE 或逐行配合 re 解析
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# sample_config = '''
# app config
# host=localhost
# port=8080
# debug=true
#
# comment line
# '''
# print(parse_simple_config(sample_config))


print("\n正则表达式进阶练习：请依次完成 TODO，并取消注释测试代码进行验证。")

