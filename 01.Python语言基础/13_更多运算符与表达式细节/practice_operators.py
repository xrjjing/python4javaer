#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更多运算符与表达式细节练习题
练习：成员运算符、身份运算符、海象运算符、解包、运算符重载
"""

# ========== 练习1：成员运算符 ==========
print("=== 练习1：成员检查 ===")
"""
题目：使用成员运算符 in / not in 完成以下任务
要求：
1. 函数 has_permission(user, permission) 检查用户是否有指定权限
   user = {"name": "张三", "permissions": ["read", "write"]}
2. 函数 is_valid_email(email) 检查邮箱是否包含 @ 和 .
3. 函数 contains_keyword(text, keyword) 检查文本是否包含关键词（不区分大小写）
"""


def has_permission(user, permission):
    """
    检查用户权限

    Args:
        user: 用户字典
        permission: 权限名称

    Returns:
        bool: 是否有权限
    """
    # TODO: 在这里实现你的代码
    pass


def is_valid_email(email):
    """
    简单的邮箱验证

    Args:
        email: 邮箱地址

    Returns:
        bool: 是否有效
    """
    # TODO: 在这里实现你的代码
    pass


def contains_keyword(text, keyword):
    """
    检查是否包含关键词（不区分大小写）

    Args:
        text: 文本
        keyword: 关键词

    Returns:
        bool: 是否包含
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
user = {"name": "张三", "permissions": ["read", "write", "delete"]}
print(f"用户有read权限：{has_permission(user, 'read')}")
print(f"用户有admin权限：{has_permission(user, 'admin')}")

print(f"\n'test@example.com' 是有效邮箱：{is_valid_email('test@example.com')}")
print(f"'invalid-email' 是有效邮箱：{is_valid_email('invalid-email')}")

text = "Python是一门强大的编程语言"
print(f"\n文本包含'Python'：{contains_keyword(text, 'python')}")
print(f"文本包含'Java'：{contains_keyword(text, 'java')}")


# ========== 练习2：身份运算符 ==========
print("\n=== 练习2：对象比较 ===")
"""
题目：理解 == 和 is 的区别
要求：
1. 函数 compare_objects(obj1, obj2) 返回字典：
   {"equal": obj1 == obj2, "identical": obj1 is obj2}
2. 测试不同类型的对象比较
3. 解释为什么有些对象 == 为True但 is 为False
"""


def compare_objects(obj1, obj2):
    """
    比较两个对象

    Args:
        obj1: 对象1
        obj2: 对象2

    Returns:
        dict: 比较结果
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
# 列表比较
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print("列表比较：")
result = compare_objects(list1, list2)
print(f"  list1 vs list2: {result}")
result = compare_objects(list1, list3)
print(f"  list1 vs list3: {result}")

# 小整数比较
num1 = 256
num2 = 256
print("\n小整数(256)比较：")
print(f"  {compare_objects(num1, num2)}")

# 大整数比较
num3 = 257
num4 = 257
print("大整数(257)比较：")
print(f"  {compare_objects(num3, num4)}")


# ========== 练习3：海象运算符 :=（Python 3.8+） ==========
print("\n=== 练习3：海象运算符应用 ===")
"""
题目：使用海象运算符简化代码
要求：
1. 使用海象运算符在 if 语句中赋值并判断
2. 函数 process_data(data) 处理数据列表：
   - 如果数据长度 > 5，打印长度并返回前5个
   - 否则返回全部数据
3. 函数 validate_input(value) 验证输入：
   - 使用海象运算符在 while 条件中处理输入
"""


def process_data(data):
    """
    处理数据

    Args:
        data: 数据列表

    Returns:
        list: 处理后的数据
    """
    # TODO: 使用海象运算符实现
    # 提示：if (length := len(data)) > 5:
    pass


def validate_input(value):
    """
    验证输入（数字必须在1-100之间）

    Args:
        value: 输入值

    Returns:
        int: 有效的值
    """
    # TODO: 使用海象运算符实现
    pass


# 测试代码
data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
data2 = [1, 2, 3]

print(f"处理长数据: {process_data(data1)}")
print(f"处理短数据: {process_data(data2)}")

print(f"\n验证输入50: {validate_input(50)}")
print(f"验证输入150: {validate_input(150)}")


# ========== 练习4：解包运算符 ==========
print("\n=== 练习4：解包操作 ===")
"""
题目：使用 * 和 ** 解包运算符
要求：
1. 函数 merge_lists(*lists) 合并任意数量的列表
2. 函数 merge_configs(**configs) 合并多个配置字典
3. 函数 print_info(name, age, **kwargs) 打印信息，接受额外的关键字参数
4. 使用解包调用函数
"""


def merge_lists(*lists):
    """
    合并多个列表

    Args:
        *lists: 任意数量的列表

    Returns:
        list: 合并后的列表
    """
    # TODO: 在这里实现你的代码
    pass


def merge_configs(**configs):
    """
    合并配置

    Args:
        **configs: 关键字参数形式的配置

    Returns:
        dict: 合并后的配置
    """
    # TODO: 在这里实现你的代码
    pass


def print_info(name, age, **kwargs):
    """
    打印信息

    Args:
        name: 姓名
        age: 年龄
        **kwargs: 其他信息
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]
merged = merge_lists(list1, list2, list3)
print(f"合并列表: {merged}")

config = merge_configs(host="localhost", port=8080, debug=True, timeout=30)
print(f"\n配置: {config}")

user_info = {"email": "test@example.com", "city": "北京", "hobby": "编程"}
print("\n用户信息:")
print_info("张三", 25, **user_info)


# ========== 练习5：扩展解包 ==========
print("\n=== 练习5：变量解包 ===")
"""
题目：使用扩展解包处理序列
要求：
1. 从列表 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 解包：
   - first, *middle, last
2. 从字符串 "Python" 解包：
   - first, *rest
3. 函数 calculate_stats(numbers) 返回：
   - min, max, 其他数字的平均值
"""


def calculate_stats(numbers):
    """
    计算统计信息

    Args:
        numbers: 数字列表（已排序）

    Returns:
        tuple: (最小值, 最大值, 中间值平均值)
    """
    # TODO: 在这里实现你的代码
    # 提示：使用扩展解包提取 first, *middle, last
    pass


# 测试代码
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# TODO: 解包 first, *middle, last
# print(f"first={first}, middle={middle}, last={last}")

text = "Python"
# TODO: 解包 first_char, *rest_chars
# print(f"首字母={first_char}, 其余={''.join(rest_chars)}")

data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
min_val, max_val, avg = calculate_stats(data)
print(f"最小值={min_val}, 最大值={max_val}, 中间平均值={avg:.1f}")


# ========== 练习6：运算符重载 ==========
print("\n=== 练习6：复数类 ===")
"""
题目：创建复数类 ComplexNumber，实现运算符重载
要求：
1. 属性：real（实部）、imag（虚部）
2. 重载 __add__ 实现加法
3. 重载 __sub__ 实现减法
4. 重载 __mul__ 实现乘法
5. 重载 __str__ 实现字符串表示（如 "3+4i"）
6. 重载 __eq__ 实现相等比较
"""


class ComplexNumber:
    """复数类"""

    def __init__(self, real, imag):
        """
        初始化复数

        Args:
            real: 实部
            imag: 虚部
        """
        # TODO: 在这里实现你的代码
        pass

    def __add__(self, other):
        """加法：(a+bi) + (c+di) = (a+c) + (b+d)i"""
        # TODO: 在这里实现你的代码
        pass

    def __sub__(self, other):
        """减法：(a+bi) - (c+di) = (a-c) + (b-d)i"""
        # TODO: 在这里实现你的代码
        pass

    def __mul__(self, other):
        """乘法：(a+bi) * (c+di) = (ac-bd) + (ad+bc)i"""
        # TODO: 在这里实现你的代码
        pass

    def __str__(self):
        """字符串表示"""
        # TODO: 在这里实现你的代码
        pass

    def __eq__(self, other):
        """相等比较"""
        # TODO: 在这里实现你的代码
        pass


# 测试代码
c1 = ComplexNumber(3, 4)
c2 = ComplexNumber(1, 2)

print(f"c1 = {c1}")
print(f"c2 = {c2}")
print(f"c1 + c2 = {c1 + c2}")
print(f"c1 - c2 = {c1 - c2}")
print(f"c1 * c2 = {c1 * c2}")
print(f"c1 == c2: {c1 == c2}")


# ========== 练习7：三元运算符和链式比较 ==========
print("\n=== 练习7：条件表达式 ===")
"""
题目：使用三元运算符和链式比较
要求：
1. 函数 get_grade(score) 使用嵌套三元运算符返回等级：
   - >= 90: "A"
   - >= 80: "B"
   - >= 70: "C"
   - >= 60: "D"
   - < 60: "F"
2. 函数 is_valid_score(score) 使用链式比较检查分数是否在 0-100 之间
3. 函数 classify_number(n) 使用三元运算符分类：
   - n > 0: "正数"
   - n < 0: "负数"
   - n == 0: "零"
"""


def get_grade(score):
    """
    获取成绩等级

    Args:
        score: 分数

    Returns:
        str: 等级
    """
    # TODO: 使用嵌套三元运算符实现
    pass


def is_valid_score(score):
    """
    验证分数是否有效

    Args:
        score: 分数

    Returns:
        bool: 是否有效
    """
    # TODO: 使用链式比较实现
    pass


def classify_number(n):
    """
    分类数字

    Args:
        n: 数字

    Returns:
        str: 分类结果
    """
    # TODO: 使用三元运算符实现
    pass


# 测试代码
scores = [95, 85, 75, 65, 55]
print("成绩等级：")
for score in scores:
    print(f"  {score}分 -> {get_grade(score)}")

print("\n分数验证：")
test_scores = [-10, 50, 100, 150]
for score in test_scores:
    print(f"  {score}: {is_valid_score(score)}")

print("\n数字分类：")
numbers = [10, -5, 0, 3.14, -2.5]
for num in numbers:
    print(f"  {num}: {classify_number(num)}")


# ========== 练习8：布尔运算的返回值 ==========
print("\n=== 练习8：默认值处理 ===")
"""
题目：利用布尔运算的返回值特性
要求：
1. 函数 get_name(user) 返回用户名，如果为空返回 "匿名用户"
2. 函数 get_config(key, configs, default) 获取配置值，不存在时返回默认值
3. 函数 first_true(*values) 返回第一个真值，都为假时返回 None
"""


def get_name(user):
    """
    获取用户名

    Args:
        user: 用户字典，包含 name 键

    Returns:
        str: 用户名或"匿名用户"
    """
    # TODO: 使用 or 运算符实现
    pass


def get_config(key, configs, default=None):
    """
    获取配置值

    Args:
        key: 配置键
        configs: 配置字典
        default: 默认值

    Returns:
        配置值或默认值
    """
    # TODO: 使用 or 运算符实现
    pass


def first_true(*values):
    """
    返回第一个真值

    Args:
        *values: 值列表

    Returns:
        第一个真值或None
    """
    # TODO: 在这里实现你的代码
    pass


# 测试代码
user1 = {"name": "张三"}
user2 = {"name": ""}
user3 = {}

print(f"用户1名称: {get_name(user1)}")
print(f"用户2名称: {get_name(user2)}")
# print(f"用户3名称: {get_name(user3)}")  # 需要处理KeyError

configs = {"host": "localhost", "port": 8080}
print(f"\n主机: {get_config('host', configs)}")
print(f"端口: {get_config('port', configs)}")
print(f"超时: {get_config('timeout', configs, 30)}")

print(f"\n第一个真值: {first_true(0, '', None, 'hello', 'world')}")
print(f"第一个真值: {first_true(0, False, [], {})}")


print("\n更多运算符与表达式细节练习完成！")
print("\n提示：完成所有TODO部分后，运行此文件查看结果")
