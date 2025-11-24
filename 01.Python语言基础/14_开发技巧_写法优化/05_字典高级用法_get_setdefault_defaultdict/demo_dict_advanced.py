"""字典高级用法示例。"""

from collections import defaultdict

user = {"name": "Tom"}
age = user.get("age", 18)
print("age:", age)

grouped: dict[str, list[int]] = {}
for key, value in [("a", 1), ("a", 2), ("b", 3)]:
    grouped.setdefault(key, []).append(value)
print("grouped with setdefault:", grouped)

dd = defaultdict(list)
for key, value in [("a", 1), ("a", 2), ("b", 3)]:
    dd[key].append(value)
print("grouped with defaultdict:", dict(dd))


