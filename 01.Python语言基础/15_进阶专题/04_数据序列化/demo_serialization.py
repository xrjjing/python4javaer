#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据序列化示例
演示：JSON、CSV、pickle、配置文件处理
"""

import os
import json
import csv
import pickle
from pathlib import Path

# ========== 1. JSON - 最常用的数据交换格式 ==========
print("=== JSON 序列化 ===")

# Python对象 → JSON
data = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "Java", "SQL"],
    "is_employed": True,
    "salary": None,
    "education": {
        "degree": "本科",
        "university": "清华大学"
    }
}

# 转换为JSON字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("JSON字符串：")
print(json_str)

# JSON字符串 → Python对象
parsed_data = json.loads(json_str)
print(f"\n解析后的数据：{parsed_data}")

# 写入JSON文件
json_file = "data.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\n已写入文件：{json_file}")

# 从JSON文件读取
with open(json_file, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
print(f"从文件加载：{loaded_data['name']}")

# 清理
os.remove(json_file)

# JSON的限制和处理
print("\n--- JSON的限制 ---")
from datetime import datetime
from decimal import Decimal

# 自定义JSON编码器
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

complex_data = {
    "timestamp": datetime.now(),
    "amount": Decimal("123.45")
}

json_str = json.dumps(complex_data, cls=CustomJSONEncoder, indent=2)
print(f"自定义编码：{json_str}")


# ========== 2. CSV - 表格数据 ==========
print("\n\n=== CSV 文件处理 ===")

csv_file = "employees.csv"

# 写入CSV - 使用DictWriter
employees = [
    {"name": "张三", "department": "技术部", "salary": 12000, "age": 28},
    {"name": "李四", "department": "销售部", "salary": 15000, "age": 30},
    {"name": "王五", "department": "财务部", "salary": 10000, "age": 26},
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "department", "salary", "age"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()  # 写入表头
    writer.writerows(employees)

print(f"已写入CSV文件：{csv_file}")

# 读取CSV - 使用DictReader
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("\n读取CSV数据：")
    for row in reader:
        print(f"  {row['name']}: {row['department']}, ¥{row['salary']}")

# 使用csv.reader/writer（列表方式）
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)
    print(f"\n列表方式读取：{len(rows)}行")

# 清理
os.remove(csv_file)


# ========== 3. pickle - Python对象序列化 ==========
print("\n\n=== pickle 序列化 ===")

# pickle可以序列化几乎所有Python对象
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

person = Person("张三", 25)
pickle_file = "person.pkl"

# 序列化到文件
with open(pickle_file, "wb") as f:
    pickle.dump(person, f)
print(f"已序列化对象：{person}")

# 从文件反序列化
with open(pickle_file, "rb") as f:
    loaded_person = pickle.load(f)
print(f"反序列化对象：{loaded_person}")

# 序列化为字节串
bytes_data = pickle.dumps(person)
print(f"字节串长度：{len(bytes_data)}")

# 清理
os.remove(pickle_file)

# pickle注意事项
print("\n--- pickle注意事项 ---")
print("优点：")
print("  - 可以序列化几乎所有Python对象")
print("  - 保持对象的完整性")
print("\n缺点：")
print("  - 只能在Python中使用")
print("  - 不同Python版本可能不兼容")
print("  - 安全风险：不要加载不可信的pickle数据")


# ========== 4. 配置文件处理 ==========
print("\n\n=== 配置文件处理 ===")

# 4.1 ConfigParser - INI格式
from configparser import ConfigParser

config = ConfigParser()

# 创建配置
config['DEFAULT'] = {
    'ServerAliveInterval': '45',
    'Compression': 'yes',
}
config['database'] = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': 'secret'
}
config['server'] = {
    'host': '0.0.0.0',
    'port': '8080',
    'debug': 'true'
}

# 写入INI文件
ini_file = "config.ini"
with open(ini_file, "w", encoding="utf-8") as f:
    config.write(f)
print(f"已创建INI配置文件：{ini_file}")

# 读取INI文件
config_read = ConfigParser()
config_read.read(ini_file, encoding="utf-8")

print("\n读取配置：")
print(f"  数据库主机：{config_read['database']['host']}")
print(f"  数据库端口：{config_read.getint('database', 'port')}")
print(f"  服务器调试：{config_read.getboolean('server', 'debug')}")

# 清理
os.remove(ini_file)


# ========== 5. 综合示例：数据导入导出 ==========
print("\n\n=== 综合示例：用户数据管理 ===")

class UserDataManager:
    """用户数据管理器"""

    def __init__(self, data_dir="user_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_as_json(self, users, filename="users.json"):
        """保存为JSON"""
        file_path = self.data_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print(f"JSON保存成功：{file_path}")

    def load_from_json(self, filename="users.json"):
        """从JSON加载"""
        file_path = self.data_dir / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def export_to_csv(self, users, filename="users.csv"):
        """导出为CSV"""
        file_path = self.data_dir / filename
        if not users:
            return

        fieldnames = users[0].keys()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        print(f"CSV导出成功：{file_path}")

    def import_from_csv(self, filename="users.csv"):
        """从CSV导入"""
        file_path = self.data_dir / filename
        users = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(dict(row))
        print(f"CSV导入成功：{len(users)}条记录")
        return users

    def cleanup(self):
        """清理测试文件"""
        import shutil
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)


# 使用示例
manager = UserDataManager()

users = [
    {"id": "1", "name": "张三", "email": "zhang@example.com", "age": "25"},
    {"id": "2", "name": "李四", "email": "li@example.com", "age": "30"},
    {"id": "3", "name": "王五", "email": "wang@example.com", "age": "28"},
]

# 保存和加载JSON
manager.save_as_json(users)
loaded_users = manager.load_from_json()
print(f"加载了{len(loaded_users)}个用户")

# 导出和导入CSV
manager.export_to_csv(users)
imported_users = manager.import_from_csv()
print(f"导入了{len(imported_users)}个用户")

# 清理
manager.cleanup()


# ========== 6. 格式选择指南 ==========
print("\n\n=== 格式选择指南 ===")
print("""
格式      | 优点                    | 缺点                | 适用场景
---------|------------------------|---------------------|------------------
JSON     | 通用、可读性好、跨语言    | 无法表示复杂类型      | API数据交换、配置
CSV      | 表格数据、Excel兼容      | 结构简单、无嵌套      | 数据导入导出、报表
pickle   | 完整的Python对象序列化   | 仅Python、安全风险    | 缓存、Python程序间
INI      | 简单配置、可读性好       | 功能受限             | 应用配置文件
""")


print("\n数据序列化演示完成！")
