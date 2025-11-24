"""解包运算符 * 与 ** 示例。"""


def add(a: int, b: int) -> int:
    return a + b


nums = [1, 2]
print("add(*nums):", add(*nums))

a = [1, 2]
b = [3, 4]
merged_list = [*a, *b]
print("merged_list:", merged_list)

default_cfg = {"timeout": 5, "retries": 2}
user_cfg = {"timeout": 10}
cfg = {**default_cfg, **user_cfg}
print("cfg:", cfg)


