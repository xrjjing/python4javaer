#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习题：序列与集合类型
"""

# 练习1：学生成绩管理
print("=== 练习1：学生成绩管理 ===")
students = ["张三", "李四", "王五", "赵六"]
scores = [85, 92, 78, 90]

# 使用 zip 合并姓名和成绩
for name, score in zip(students, scores):
    print(f"{name}: {score}分")

# 计算平均分
avg_score = sum(scores) / len(scores)
print(f"平均分：{avg_score:.2f}")

# 找出最高分和最低分
max_score = max(scores)
min_score = min(scores)
max_idx = scores.index(max_score)
min_idx = scores.index(min_score)

print(f"最高分：{students[max_idx]}，{max_score}分")
print(f"最低分：{students[min_idx]}，{min_score}分")

# 练习2：商品库存管理
print("\n=== 练习2：商品库存管理 ===")
products = {
    "苹果": {"price": 5.5, "stock": 100},
    "香蕉": {"price": 3.8, "stock": 80},
    "橙子": {"price": 4.2, "stock": 120},
    "葡萄": {"price": 8.9, "stock": 50},
}

print("商品信息：")
for name, info in products.items():
    print(f"{name}：单价{info['price']}元，库存{info['stock']}件")

# 计算总库存价值
total_value = 0
for name, info in products.items():
    value = info['price'] * info['stock']
    total_value += value
    print(f"{name}总价值：{value:.2f}元")

print(f"\n仓库总价值：{total_value:.2f}元")

# 练习3：去重并排序
print("\n=== 练习3：列表去重并排序 ===")
numbers = [5, 3, 9, 1, 3, 5, 8, 2, 9, 7]
print(f"原列表：{numbers}")

# 方法1：使用set去重，然后排序
unique1 = sorted(set(numbers))
print(f"去重并排序（方法1）：{unique1}")

# 方法2：使用临时集合判断
unique2 = []
for num in numbers:
    if num not in unique2:
        unique2.append(num)
unique2.sort()
print(f"去重并排序（方法2）：{unique2}")

# 练习4：频次统计
print("\n=== 练习4：字符频次统计 ===")
text = "hello world"
print(f"文本：'{text}'")

# 方法1：使用字典
freq1 = {}
for char in text:
    freq1[char] = freq1.get(char, 0) + 1
print(f"频次统计（方法1）：{freq1}")

# 方法2：使用Counter（需要导入）
from collections import Counter
freq2 = Counter(text)
print(f"频次统计（方法2）：{dict(freq2)}")

# 练习5：商品推荐系统
print("\n=== 练习5：商品推荐 ===")
# 用户购买历史
user_history = [
    {"user": "用户A", "purchases": ["苹果", "香蕉", "橙子"]},
    {"user": "用户B", "purchases": ["香蕉", "葡萄", "苹果"]},
    {"user": "用户C", "purchases": ["橙子", "葡萄", "西瓜"]},
]

# 统计商品共同购买关系
pair_count = {}
for record in user_history:
    purchases = record["purchases"]
    for i in range(len(purchases)):
        for j in range(i + 1, len(purchases)):
            item1, item2 = purchases[i], purchases[j]
            pair = tuple(sorted([item1, item2]))
            pair_count[pair] = pair_count.get(pair, 0) + 1

print("商品共同购买统计：")
for (item1, item2), count in pair_count.items():
    print(f"  {item1} - {item2}: {count}次")

# 为新用户推荐
new_user_purchases = ["苹果"]
print(f"\n基于'{new_user_purchases}'的推荐：")
recommendations = {}
for item in new_user_purchases:
    for pair, count in pair_count.items():
        if item in pair:
            other_item = pair[0] if pair[1] == item else pair[1]
            recommendations[other_item] = recommendations.get(other_item, 0) + count

# 输出推荐结果（排除已购买）
for item, count in sorted(recommendations.items(), key=lambda x: x[1], reverse=True):
    if item not in new_user_purchases:
        print(f"  推荐：{item} (相似度：{count})")

# 练习6：矩阵运算
print("\n=== 练习6：矩阵加法 ===")
# 两个2x2矩阵
matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]

print("矩阵1：")
for row in matrix1:
    print(row)

print("矩阵2：")
for row in matrix2:
    print(row)

# 矩阵加法
result = []
for i in range(2):
    row = []
    for j in range(2):
        row.append(matrix1[i][j] + matrix2[i][j])
    result.append(row)

print("矩阵加法结果：")
for row in result:
    print(row)

# 练习7：名片夹管理
print("\n=== 练习7：名片夹管理 ===")
contacts = {}

# 添加联系人
contacts["张三"] = {"phone": "13800138001", "email": "zhangsan@example.com"}
contacts["李四"] = {"phone": "13800138002", "email": "lisi@example.com"}
contacts["王五"] = {"phone": "13800138003", "email": "wangwu@example.com"}

print("联系人列表：")
for name, info in contacts.items():
    print(f"{name}：{info['phone']}，{info['email']}")

# 查找联系人
search_name = "张三"
if search_name in contacts:
    print(f"\n找到联系人：{search_name}")
    print(f"  电话：{contacts[search_name]['phone']}")
    print(f"  邮箱：{contacts[search_name]['email']}")
else:
    print(f"\n未找到联系人：{search_name}")

# 删除联系人
del_contacts = "李四"
if del_contacts in contacts:
    del contacts[del_contacts]
    print(f"\n已删除联系人：{del_contacts}")

print(f"\n剩余联系人数量：{len(contacts)}")

# 练习8：学生成绩分析
print("\n=== 练习8：学生成绩分析 ===")
students_data = {
    "张三": {"数学": 85, "语文": 90, "英语": 78},
    "李四": {"数学": 92, "语文": 88, "英语": 95},
    "王五": {"数学": 78, "语文": 85, "英语": 82},
}

# 计算每个学生的平均分
print("学生平均分：")
for name, scores in students_data.items():
    avg = sum(scores.values()) / len(scores)
    print(f"{name}：{avg:.2f}分")

# 计算每门课的平均分
subjects = ["数学", "语文", "英语"]
for subject in subjects:
    total = sum(students_data[name][subject] for name in students_data)
    avg = total / len(students_data)
    print(f"{subject}平均分：{avg:.2f}分")
