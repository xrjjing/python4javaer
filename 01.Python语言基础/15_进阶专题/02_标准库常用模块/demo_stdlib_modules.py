#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准库常用模块示例
演示：datetime、collections、itertools、functools
"""

# ========== 1. datetime - 日期时间处理 ==========
print("=== datetime 模块 ===")
from datetime import datetime, date, time, timedelta, timezone

# 获取当前时间
now = datetime.now()
print(f"当前时间：{now}")
print(f"当前日期：{date.today()}")

# 创建特定日期时间
specific_date = datetime(2024, 12, 25, 10, 30, 0)
print(f"\n特定时间：{specific_date}")

# 格式化输出
print(f"格式化：{now.strftime('%Y年%m月%d日 %H:%M:%S')}")
print(f"ISO格式：{now.isoformat()}")

# 解析字符串
date_str = "2024-12-25"
parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
print(f"\n解析日期：{parsed_date}")

# 日期运算
tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
yesterday = now - timedelta(days=1)

print(f"\n明天：{tomorrow.strftime('%Y-%m-%d')}")
print(f"下周：{next_week.strftime('%Y-%m-%d')}")
print(f"昨天：{yesterday.strftime('%Y-%m-%d')}")

# 计算日期差
date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 12, 31)
diff = date2 - date1
print(f"\n日期差：{diff.days}天")

# 时区处理
utc_now = datetime.now(timezone.utc)
print(f"\nUTC时间：{utc_now}")

# 常用日期判断
print(f"\n今天是星期{now.weekday() + 1}")  # 0=周一
print(f"今年第{now.timetuple().tm_yday}天")


# ========== 2. collections - 特殊容器 ==========
print("\n\n=== collections 模块 ===")
from collections import Counter, defaultdict, namedtuple, deque, OrderedDict

# Counter - 计数器
print("--- Counter 计数器 ---")
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
counter = Counter(words)
print(f"词频统计：{counter}")
print(f"最常见的2个：{counter.most_common(2)}")
print(f"apple出现次数：{counter['apple']}")

# 计数器运算
counter1 = Counter(["a", "b", "c", "a", "b", "b"])
counter2 = Counter(["b", "c", "d", "c", "c"])
print(f"\nCounter相加：{counter1 + counter2}")
print(f"Counter相减：{counter1 - counter2}")

# defaultdict - 默认值字典
print("\n--- defaultdict 默认值字典 ---")
dd = defaultdict(int)  # 默认值为0
dd['a'] += 1
dd['b'] += 2
dd['c'] += 3
print(f"defaultdict(int)：{dict(dd)}")

# 分组
students_by_class = defaultdict(list)
students = [("张三", "1班"), ("李四", "2班"), ("王五", "1班"), ("赵六", "2班")]
for name, class_name in students:
    students_by_class[class_name].append(name)
print(f"按班级分组：{dict(students_by_class)}")

# namedtuple - 命名元组
print("\n--- namedtuple 命名元组 ---")
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(f"点坐标：{p}")
print(f"x坐标：{p.x}, y坐标：{p.y}")
print(f"距离：{(p.x**2 + p.y**2)**0.5:.2f}")

Person = namedtuple('Person', ['name', 'age', 'city'])
person = Person('张三', 25, '北京')
print(f"\n人员信息：{person}")
print(f"姓名：{person.name}")

# deque - 双端队列
print("\n--- deque 双端队列 ---")
dq = deque([1, 2, 3, 4, 5])
print(f"初始队列：{dq}")

dq.append(6)  # 右端添加
dq.appendleft(0)  # 左端添加
print(f"两端添加后：{dq}")

dq.pop()  # 右端删除
dq.popleft()  # 左端删除
print(f"两端删除后：{dq}")

# 限制长度的deque（自动删除旧元素）
limited_dq = deque(maxlen=3)
for i in range(5):
    limited_dq.append(i)
    print(f"添加{i}后：{limited_dq}")

# rotate - 旋转
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)  # 向右旋转2位
print(f"\n向右旋转2位：{dq}")


# ========== 3. itertools - 迭代工具 ==========
print("\n\n=== itertools 模块 ===")
from itertools import (
    count, cycle, repeat, chain, combinations, permutations,
    product, islice, groupby, accumulate, zip_longest
)

# count - 无限计数
print("--- count 无限计数 ---")
for i in islice(count(10, 2), 5):  # 从10开始，步长2，取5个
    print(i, end=" ")
print()

# cycle - 循环迭代
print("\n--- cycle 循环 ---")
colors = cycle(['红', '黄', '绿'])
for _ in range(7):
    print(next(colors), end=" ")
print()

# repeat - 重复元素
print("\n--- repeat 重复 ---")
print(list(repeat('A', 5)))

# chain - 连接迭代器
print("\n--- chain 连接 ---")
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]
print(f"连接三个列表：{list(chain(list1, list2, list3))}")

# combinations - 组合
print("\n--- combinations 组合 ---")
items = ['A', 'B', 'C', 'D']
print(f"4个元素的2元组合：{list(combinations(items, 2))}")

# permutations - 排列
print("\n--- permutations 排列 ---")
items = ['A', 'B', 'C']
print(f"3个元素的2元排列：{list(permutations(items, 2))}")

# product - 笛卡尔积
print("\n--- product 笛卡尔积 ---")
print(f"['A','B'] × [1,2]：{list(product(['A', 'B'], [1, 2]))}")

# groupby - 分组
print("\n--- groupby 分组 ---")
data = [
    ('张三', 'A'),
    ('李四', 'A'),
    ('王五', 'B'),
    ('赵六', 'B'),
    ('钱七', 'A'),
]
# 注意：groupby需要先排序
data.sort(key=lambda x: x[1])
for key, group in groupby(data, key=lambda x: x[1]):
    print(f"{key}组：{[name for name, _ in group]}")

# accumulate - 累积
print("\n--- accumulate 累积 ---")
numbers = [1, 2, 3, 4, 5]
print(f"累积和：{list(accumulate(numbers))}")
print(f"累积积：{list(accumulate(numbers, lambda x, y: x * y))}")

# zip_longest - 长度不等的zip
print("\n--- zip_longest ---")
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c', 'd', 'e']
print(f"zip_longest：{list(zip_longest(list1, list2, fillvalue=0))}")


# ========== 4. functools - 函数工具 ==========
print("\n\n=== functools 模块 ===")
from functools import reduce, partial, wraps, lru_cache, total_ordering

# reduce - 归约
print("--- reduce 归约 ---")
numbers = [1, 2, 3, 4, 5]
sum_result = reduce(lambda x, y: x + y, numbers)
product_result = reduce(lambda x, y: x * y, numbers)
print(f"列表求和：{sum_result}")
print(f"列表求积：{product_result}")

# partial - 偏函数
print("\n--- partial 偏函数 ---")
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"5的平方：{square(5)}")
print(f"5的立方：{cube(5)}")

# lru_cache - 缓存装饰器
print("\n--- lru_cache 缓存 ---")
@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"fibonacci(10)：{fibonacci(10)}")
print(f"fibonacci(20)：{fibonacci(20)}")
print(f"缓存信息：{fibonacci.cache_info()}")

# total_ordering - 自动生成比较方法
print("\n--- total_ordering ---")
@total_ordering
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f"{self.name}({self.score}分)"

students = [
    Student("张三", 85),
    Student("李四", 92),
    Student("王五", 78),
]
students.sort()
print(f"学生排序：{students}")


# ========== 5. 综合示例 ==========
print("\n\n=== 综合示例：日志分析 ===")
from collections import Counter, defaultdict
from datetime import datetime
from itertools import groupby

# 模拟日志数据
logs = [
    "2024-01-01 10:30:00 ERROR Database connection failed",
    "2024-01-01 10:31:00 INFO User login successful",
    "2024-01-01 10:32:00 WARNING Memory usage high",
    "2024-01-01 10:33:00 ERROR File not found",
    "2024-01-01 10:34:00 INFO Data saved",
    "2024-01-01 10:35:00 ERROR Network timeout",
    "2024-01-02 09:00:00 INFO System started",
    "2024-01-02 09:15:00 WARNING Disk space low",
]

# 解析日志
parsed_logs = []
for log in logs:
    parts = log.split(maxsplit=3)
    date_str = f"{parts[0]} {parts[1]}"
    level = parts[2]
    message = parts[3]

    parsed_logs.append({
        'datetime': datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"),
        'level': level,
        'message': message
    })

# 统计各级别日志数量
level_counter = Counter(log['level'] for log in parsed_logs)
print(f"日志级别统计：{level_counter}")

# 按日期分组
logs_by_date = defaultdict(list)
for log in parsed_logs:
    date_key = log['datetime'].date()
    logs_by_date[date_key].append(log)

print(f"\n按日期分组：")
for date_key, logs in logs_by_date.items():
    print(f"  {date_key}：{len(logs)}条日志")

# 找出所有ERROR级别的日志
errors = [log for log in parsed_logs if log['level'] == 'ERROR']
print(f"\nERROR日志：")
for error in errors:
    print(f"  {error['datetime']} - {error['message']}")


print("\n标准库常用模块演示完成！")
