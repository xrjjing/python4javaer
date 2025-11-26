#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块与包基础示例
演示：import、from...import、__name__、模块搜索路径、包结构
"""

# 1. 导入标准库模块
print("=== 导入标准库模块 ===")
import math
import random
import datetime

# 使用 math 模块
print(f"圆周率：{math.pi}")
print(f"平方根 sqrt(16)：{math.sqrt(16)}")
print(f"向上取整 ceil(3.2)：{math.ceil(3.2)}")

# 使用 random 模块
print(f"\n随机整数：{random.randint(1, 100)}")
print(f"随机选择：{random.choice(['苹果', '香蕉', '橙子'])}")

# 使用 datetime 模块
now = datetime.datetime.now()
print(f"\n当前时间：{now}")
print(f"格式化时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")

# 2. from...import 导入特定内容
print("\n=== from...import 导入 ===")
from math import sqrt, pi, sin
from random import randint, choice

print(f"直接使用 pi：{pi}")
print(f"直接使用 sqrt(25)：{sqrt(25)}")
print(f"sin(pi/2)：{sin(pi/2)}")

# 3. 使用别名
print("\n=== 使用别名 ===")
import datetime as dt
import numpy as np  # 如果安装了numpy

today = dt.date.today()
print(f"今天日期：{today}")

# 4. 导入所有内容（不推荐）
print("\n=== 导入所有内容（不推荐）===")
# from math import *  # 不推荐，会污染命名空间
# print(sqrt(9))  # 可以直接使用，但不知道来自哪个模块

# 5. __name__ 变量
print("\n=== __name__ 变量 ===")
print(f"当前模块的 __name__：{__name__}")

def main():
    """主函数"""
    print("这是主函数")

# 只有直接运行此脚本时才执行
if __name__ == "__main__":
    print("直接运行此脚本")
    main()
else:
    print("此模块被导入")

# 6. 查看模块属性
print("\n=== 查看模块属性 ===")
print(f"math 模块的部分属性：")
math_attrs = [attr for attr in dir(math) if not attr.startswith('_')]
print(f"前10个：{math_attrs[:10]}")

# 7. 模块搜索路径
print("\n=== 模块搜索路径 ===")
import sys
print("Python 模块搜索路径（前3个）：")
for i, path in enumerate(sys.path[:3], 1):
    print(f"{i}. {path}")

# 8. 创建自定义模块示例
print("\n=== 自定义模块示例 ===")
# 创建一个临时模块文件
import os

# 创建 my_utils.py 模块
module_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自定义工具模块"""

def greet(name):
    """问候函数"""
    return f"你好，{name}！"

def add(a, b):
    """加法函数"""
    return a + b

PI = 3.14159

class Calculator:
    """简单计算器类"""
    @staticmethod
    def multiply(a, b):
        return a * b

if __name__ == "__main__":
    print("这是 my_utils 模块")
    print(greet("测试"))
'''

# 写入临时模块文件
with open("my_utils.py", "w", encoding="utf-8") as f:
    f.write(module_content)

try:
    # 导入自定义模块
    import my_utils

    print(f"使用自定义模块：")
    print(f"  greet('张三')：{my_utils.greet('张三')}")
    print(f"  add(5, 3)：{my_utils.add(5, 3)}")
    print(f"  PI：{my_utils.PI}")
    print(f"  Calculator.multiply(4, 5)：{my_utils.Calculator.multiply(4, 5)}")

finally:
    # 清理临时文件
    if os.path.exists("my_utils.py"):
        os.remove("my_utils.py")
    if os.path.exists("__pycache__"):
        import shutil
        shutil.rmtree("__pycache__")

# 9. 包的概念
print("\n=== 包的概念 ===")
print("""
包（Package）是包含多个模块的目录，必须包含 __init__.py 文件。

示例包结构：
my_package/
    __init__.py
    module1.py
    module2.py
    sub_package/
        __init__.py
        module3.py

使用方式：
    import my_package.module1
    from my_package import module2
    from my_package.sub_package import module3
""")

# 10. 常用标准库模块
print("\n=== 常用标准库模块 ===")

# os 模块 - 操作系统接口
import os
print(f"当前工作目录：{os.getcwd()}")
print(f"操作系统类型：{os.name}")

# sys 模块 - 系统相关
import sys
print(f"Python 版本：{sys.version}")
print(f"平台：{sys.platform}")

# json 模块 - JSON 处理
import json
data = {"name": "张三", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
print(f"JSON 字符串：{json_str}")

# collections 模块 - 高级容器
from collections import Counter, defaultdict
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_count = Counter(words)
print(f"单词计数：{word_count}")

# 11. 模块重载（开发调试用）
print("\n=== 模块重载 ===")
import importlib
# importlib.reload(module_name)  # 重新加载模块
print("使用 importlib.reload() 可以重新加载已导入的模块")

# 12. 相对导入和绝对导入
print("\n=== 导入方式 ===")
print("""
绝对导入（推荐）：
    from package.module import function
    import package.module

相对导入（包内使用）：
    from . import module          # 当前包
    from .. import module         # 上级包
    from .subpackage import module  # 子包
""")

# 13. 第三方包管理
print("\n=== 第三方包管理 ===")
print("""
使用 pip 安装第三方包：
    pip install requests
    pip install pandas
    pip install numpy

查看已安装的包：
    pip list
    pip show requests

卸载包：
    pip uninstall requests

导出依赖：
    pip freeze > requirements.txt

安装依赖：
    pip install -r requirements.txt
""")

# 14. 模块的 __all__ 属性
print("\n=== __all__ 属性 ===")
print("""
在模块中定义 __all__ 可以控制 from module import * 导入的内容：

# my_module.py
__all__ = ['public_func', 'PublicClass']

def public_func():
    pass

def _private_func():  # 不会被 * 导入
    pass

class PublicClass:
    pass
""")

print("\n模块与包基础演示完成！")
