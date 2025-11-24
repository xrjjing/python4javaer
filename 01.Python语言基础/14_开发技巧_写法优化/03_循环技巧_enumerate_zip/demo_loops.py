"""enumerate 与 zip 循环示例。"""

lines = ["第一行", "第二行", "第三行"]
for index, line in enumerate(lines, start=1):
    print(f"{index}: {line}")

names = ["Tom", "Alice", "Bob"]
scores = [90, 85, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")


