"""列表 / 字典 / 集合推导式示例。"""

# 列表推导式：平方
squares = [x * x for x in range(10)]
print("squares:", squares)

# 列表推导式：过滤偶数
evens = [x for x in range(20) if x % 2 == 0]
print("evens:", evens)

# 字典推导式：数字到平方的映射
square_map = {x: x * x for x in range(5)}
print("square_map:", square_map)

# 集合推导式：名字长度去重
names = ["Tom", "Alice", "Bob", "Alice"]
lengths = {len(name) for name in names}
print("lengths:", lengths)


