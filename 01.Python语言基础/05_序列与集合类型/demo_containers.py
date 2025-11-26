#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
序列与集合类型示例
演示：list、tuple、dict、set的增删改查和切片
"""

# 1. 列表（List）- 可变序列
print("=== 列表操作 ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"初始列表：{fruits}")

# 添加元素
fruits.append("葡萄")  # 末尾添加
print(f"append('葡萄')：{fruits}")

fruits.insert(1, "梨")  # 指定位置插入
print(f"insert(1, '梨')：{fruits}")

# 修改元素
fruits[0] = "红苹果"
print(f"修改第0个元素：{fruits}")

# 删除元素
removed = fruits.pop()  # 移除最后一个
print(f"pop()：{removed}，剩余：{fruits}")

fruits.remove("梨")  # 移除指定值
print(f"remove('梨')：{fruits}")

# 切片操作
print(f"fruits[1:3]：{fruits[1:3]}")
print(f"fruits[:2]：{fruits[:2]}")
print(f"fruits[1:]：{fruits[1:]}")
print(f"fruits[::2]：{fruits[::2]}")  # 步长为2

# 列表推导式
squares = [x**2 for x in range(10)]
print(f"0-9的平方：{squares}")

# 2. 元组（Tuple）- 不可变序列
print("\n=== 元组操作 ===")
point = (3, 4)
print(f"坐标点：{point}")
print(f"x坐标：{point[0]}，y坐标：{point[1]}")

# 不可修改
# point[0] = 5  # 会报错

# 元组拆包
x, y = point
print(f"拆包：x={x}, y={y}")

# 3. 字典（Dict）- 键值对
print("\n=== 字典操作 ===")
person = {"name": "张三", "age": 25, "city": "北京"}
print(f"初始字典：{person}")

# 添加/修改
person["email"] = "zhangsan@example.com"
person["age"] = 26
print(f"添加email：{person}")

# 获取值
print(f"姓名：{person.get('name')}")
print(f"电话（不存在）：{person.get('phone', '未知')}")

# 遍历
print("遍历键值对：")
for key, value in person.items():
    print(f"  {key}: {value}")

# 常用方法
keys = list(person.keys())
values = list(person.values())
print(f"所有键：{keys}")
print(f"所有值：{values}")

# 4. 集合（Set）- 无序不重复元素
print("\n=== 集合操作 ===")
nums1 = {1, 2, 3, 4, 5}
nums2 = {3, 4, 5, 6, 7}

print(f"集合1：{nums1}")
print(f"集合2：{nums2}")

# 交集
print(f"交集：{nums1 & nums2}")
# 并集
print(f"并集：{nums1 | nums2}")
# 差集
print(f"差集 nums1 - nums2：{nums1 - nums2}")
print(f"差集 nums2 - nums1：{nums2 - nums1}")

# 添加元素
nums1.add(10)
print(f"添加10后：{nums1}")

# 列表去重
numbers = [1, 2, 2, 3, 3, 3, 4, 5]
unique_numbers = list(set(numbers))
print(f"原列表：{numbers}")
print(f"去重后：{unique_numbers}")

# 5. 字符串（str）- 不可变序列
print("\n=== 字符串操作 ===")
text = "Hello, Python!"
print(f"原字符串：{text}")
print(f"长度：{len(text)}")
print(f"转大写：{text.upper()}")
print(f"转小写：{text.lower()}")
print(f"查找'Python'：{text.find('Python')}")
print(f"替换'Python'为'World'：{text.replace('Python', 'World')}")

# 字符串分割
parts = text.split(",")
print(f"按逗号分割：{parts}")

# 6. 列表的其他操作
print("\n=== 列表其他操作 ===")
scores = [90, 85, 92, 78, 88]
print(f"成绩列表：{scores}")
print(f"最高分：{max(scores)}")
print(f"最低分：{min(scores)}")
print(f"总分：{sum(scores)}")
print(f"平均分：{sum(scores)/len(scores):.2f}")

# 排序
scores.sort()
print(f"升序排序：{scores}")

scores.sort(reverse=True)
print(f"降序排序：{scores}")

# 统计
print(f"90分出现次数：{scores.count(90)}")

# 扩展
scores2 = [95, 100]
scores.extend(scores2)
print(f"扩展scores2后：{scores}")

# 7. 字典的嵌套使用
print("\n=== 嵌套字典 ===")
students = {
    "张三": {"数学": 90, "语文": 85, "英语": 92},
    "李四": {"数学": 88, "语文": 90, "英语": 86},
}

for name, scores in students.items():
    print(f"{name}的成绩：")
    for subject, score in scores.items():
        print(f"  {subject}: {score}")

# 8. 列表的嵌套（矩阵）
print("\n=== 嵌套列表（矩阵）===")
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("3x3矩阵：")
for row in matrix:
    for num in row:
        print(f"{num:2d}", end=" ")
    print()

# 访问元素
print(f"matrix[1][1] = {matrix[1][1]}")

# 9. 推导式家族
print("\n=== 各种推导式 ===")

# 列表推导式
squares = [x**2 for x in range(10)]
print(f"列表推导式 - 平方：{squares}")

# 集合推导式
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(f"集合推导式 - 偶数平方：{even_squares}")

# 字典推导式
square_dict = {x: x**2 for x in range(5)}
print(f"字典推导式 - 平方映射：{square_dict}")
