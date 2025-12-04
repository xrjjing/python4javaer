#!/usr/bin/env python3
# 简单命令行计算器：支持加、减、乘、除


def add(x: float, y: float) -> float:
    return x + y


def subtract(x: float, y: float) -> float:
    return x - y


def multiply(x: float, y: float) -> float:
    return x * y


def divide(x: float, y: float) -> float:
    if y == 0:
        raise ZeroDivisionError("除数不能为零")
    return x / y


def read_number(prompt: str) -> float:
    """重复读取直到获得合法数字"""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("⚠️ 输入无效，请输入数字。")


def main() -> None:
    actions = {
        "1": ("加法", add),
        "2": ("减法", subtract),
        "3": ("乘法", multiply),
        "4": ("除法", divide),
        "q": ("退出", None),
    }

    print("=== 简易计算器 ===")
    while True:
        print("\n请选择操作：")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("输入选项编号 (q 退出)：").strip().lower()
        if choice == "q":
            print("再见！")
            break

        if choice not in actions or choice == "q":
            print("⚠️ 选项无效，请重新选择。")
            continue

        num1 = read_number("请输入第一个数：")
        num2 = read_number("请输入第二个数：")

        op_name, func = actions[choice]
        try:
            result = func(num1, num2)  # type: ignore[arg-type]
            print(f"结果 ({op_name}): {result}")
        except ZeroDivisionError as err:
            print(f"⚠️ 计算失败：{err}")


if __name__ == "__main__":
    main()
