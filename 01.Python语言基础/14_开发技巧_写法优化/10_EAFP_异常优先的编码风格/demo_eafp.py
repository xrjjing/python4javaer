"""EAFP 与 LBYL 风格对比示例。"""

data = {"name": "Tom"}

# LBYL：先判断再访问
if "age" in data:
    age = data["age"]
else:
    age = 18
print("LBYL age:", age)

# EAFP：直接访问，出错再处理
try:
    age2 = data["age"]
except KeyError:
    age2 = 18
print("EAFP age:", age2)


