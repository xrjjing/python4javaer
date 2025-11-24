"""any / all 示例。"""

nums = [0, -1, 3, 0]
has_positive = any(n > 0 for n in nums)
print("存在正数：", has_positive)

grades = [80, 90, 75]
all_passed = all(g >= 60 for g in grades)
print("全部及格：", all_passed)


