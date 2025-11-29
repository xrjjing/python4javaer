#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据序列化练习
练习：JSON / CSV / 配置文件
"""

from __future__ import annotations

import csv
import json
from configparser import ConfigParser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List


print("=== 练习1：JSON 配置读写 ===")
"""
题目：实现保存与加载 JSON 配置的函数
要求：
1. save_json_config(path, data)：将 data 写入指定路径（带缩进）
2. load_json_config(path)：从文件加载 JSON 并返回字典
3. 读写时使用 UTF-8 编码
"""


def save_json_config(path: Path, data: dict) -> None:
    """保存 JSON 配置文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


def load_json_config(path: Path) -> dict:
    """加载 JSON 配置文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# cfg_path = Path("config.json")
# save_json_config(cfg_path, {"debug": True, "host": "localhost"})
# print(load_json_config(cfg_path))


print("\n=== 练习2：CSV ↔ 列表字典 ===")
"""
题目：
1. 实现 write_employees_csv(path, employees)
   - employees 为包含若干字典的列表，每个字典有 name/department/salary 字段
2. 实现 read_employees_csv(path)，读取 CSV 返回员工列表（字典）
3. 使用 csv.DictWriter 和 csv.DictReader
"""


def write_employees_csv(path: Path, employees: list[dict]) -> None:
    """将员工信息写入 CSV 文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


def read_employees_csv(path: Path) -> list[dict]:
    """从 CSV 文件中读取员工信息。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# employees = [
#     {"name": "张三", "department": "技术部", "salary": 12000},
#     {"name": "李四", "department": "销售部", "salary": 15000},
# ]
# csv_path = Path("employees.csv")
# write_employees_csv(csv_path, employees)
# print(read_employees_csv(csv_path))


print("\n=== 练习3：INI 配置文件 ===")
"""
题目：
1. 使用 ConfigParser 写入一个简单配置文件 settings.ini
   - [database] section，包含 host/port/user 三个键
2. 实现 read_db_config(path)，读取并返回 dict
"""


def write_db_config(path: Path) -> None:
    """写入数据库配置到 INI 文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


def read_db_config(path: Path) -> dict:
    """从 INI 文件读取数据库配置。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n数据序列化练习：请结合《数据序列化》文档完成上述 TODO，并在本地实际读写文件进行验证。")

