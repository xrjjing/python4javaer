"""f-string 字符串格式化示例。"""

name = "Alice"
age = 25
price = 3.1415926

basic = f"你好，我是{name}，今年{age}岁。"
print(basic)

expr = f"2 + 3 = {2 + 3}"
print(expr)

formatted_price = f"价格：{price:.2f}"
print(formatted_price)


