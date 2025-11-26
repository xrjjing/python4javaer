#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命名空间、作用域与类型注解示例
演示：LEGB规则、global、nonlocal、类型注解、typing模块
"""

# 1. LEGB 作用域规则
print("=== LEGB 作用域规则 ===")
# L - Local（局部）
# E - Enclosing（嵌套）
# G - Global（全局）
# B - Built-in（内置）

x = "全局变量"  # Global

def outer():
    x = "外层函数变量"  # Enclosing

    def inner():
        x = "内层函数变量"  # Local
        print(f"内层函数：{x}")

    inner()
    print(f"外层函数：{x}")

outer()
print(f"全局：{x}")

# 2. global 关键字
print("\n=== global 关键字 ===")
count = 0

def increment():
    global count
    count += 1
    print(f"计数器：{count}")

increment()
increment()
print(f"全局计数器：{count}")

# 3. nonlocal 关键字
print("\n=== nonlocal 关键字 ===")
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        print(f"内层计数：{count}")

    inner()
    inner()
    print(f"外层计数：{count}")

outer()

# 4. 基础类型注解
print("\n=== 基础类型注解 ===")
def greet(name: str) -> str:
    """带类型注解的函数"""
    return f"你好，{name}！"

def add(a: int, b: int) -> int:
    """整数加法"""
    return a + b

def divide(a: float, b: float) -> float:
    """浮点数除法"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

print(greet("张三"))
print(f"add(3, 5) = {add(3, 5)}")
print(f"divide(10.0, 2.0) = {divide(10.0, 2.0)}")

# 5. 变量类型注解
print("\n=== 变量类型注解 ===")
name: str = "张三"
age: int = 25
height: float = 1.75
is_student: bool = True

print(f"姓名：{name}（类型：{type(name).__name__}）")
print(f"年龄：{age}（类型：{type(age).__name__}）")

# 6. 容器类型注解
print("\n=== 容器类型注解 ===")
from typing import List, Dict, Tuple, Set, Optional

# 列表
numbers: List[int] = [1, 2, 3, 4, 5]
names: List[str] = ["张三", "李四", "王五"]

# 字典
person: Dict[str, any] = {"name": "张三", "age": 25}
scores: Dict[str, int] = {"数学": 90, "语文": 85}

# 元组
point: Tuple[int, int] = (3, 4)
rgb: Tuple[int, int, int] = (255, 0, 0)

# 集合
unique_numbers: Set[int] = {1, 2, 3, 4, 5}

# Optional（可选类型）
def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """查找用户，可能返回None"""
    if user_id == 1:
        return {"name": "张三", "email": "zhang@example.com"}
    return None

user = find_user(1)
print(f"找到用户：{user}")

# 7. 函数类型注解
print("\n=== 函数类型注解 ===")
from typing import Callable

def apply_operation(a: int, b: int, operation: Callable[[int, int], int]) -> int:
    """应用操作函数"""
    return operation(a, b)

def add_func(x: int, y: int) -> int:
    return x + y

def multiply_func(x: int, y: int) -> int:
    return x * y

result1 = apply_operation(5, 3, add_func)
result2 = apply_operation(5, 3, multiply_func)
print(f"加法结果：{result1}")
print(f"乘法结果：{result2}")

# 8. 类型别名
print("\n=== 类型别名 ===")
from typing import Union

# 定义类型别名
UserId = int
UserName = str
Score = Union[int, float]  # 可以是int或float

def get_user_score(user_id: UserId) -> Score:
    """获取用户分数"""
    return 85.5

user_id: UserId = 123
score: Score = get_user_score(user_id)
print(f"用户{user_id}的分数：{score}")

# 9. 泛型
print("\n=== 泛型 ===")
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    """泛型栈"""
    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

# 整数栈
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"弹出：{int_stack.pop()}")

# 字符串栈
str_stack: Stack[str] = Stack()
str_stack.push("Hello")
str_stack.push("World")
print(f"弹出：{str_stack.pop()}")

# 10. 类的类型注解
print("\n=== 类的类型注解 ===")
class Student:
    """学生类"""
    name: str
    age: int
    scores: Dict[str, int]

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.scores = {}

    def add_score(self, subject: str, score: int) -> None:
        """添加成绩"""
        self.scores[subject] = score

    def get_average(self) -> float:
        """计算平均分"""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

student = Student("张三", 20)
student.add_score("数学", 90)
student.add_score("语文", 85)
print(f"{student.name}的平均分：{student.get_average():.2f}")

# 11. 字面量类型
print("\n=== 字面量类型 ===")
from typing import Literal

def set_status(status: Literal["pending", "running", "completed"]) -> None:
    """设置状态（只能是指定的几个值）"""
    print(f"状态设置为：{status}")

set_status("pending")
set_status("running")
# set_status("invalid")  # 类型检查器会报错

# 12. 协议（Protocol）
print("\n=== 协议 ===")
from typing import Protocol

class Drawable(Protocol):
    """可绘制协议"""
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("绘制圆形")

class Square:
    def draw(self) -> None:
        print("绘制正方形")

def render(shape: Drawable) -> None:
    """渲染形状"""
    shape.draw()

circle = Circle()
square = Square()
render(circle)
render(square)

# 13. 命名空间查看
print("\n=== 命名空间查看 ===")
def show_namespace():
    local_var = "局部变量"
    print(f"局部命名空间：{locals()}")
    print(f"全局命名空间（部分）：{list(globals().keys())[:5]}")

show_namespace()

# 14. 作用域陷阱
print("\n=== 作用域陷阱 ===")
# 陷阱1：循环变量泄漏
for i in range(3):
    pass
print(f"循环后 i 的值：{i}")  # i 仍然存在

# 陷阱2：闭包中的变量
def create_multipliers():
    multipliers = []
    for i in range(3):
        multipliers.append(lambda x: x * i)
    return multipliers

funcs = create_multipliers()
print(f"闭包陷阱：{[f(2) for f in funcs]}")  # 都是 4（2*2）

# 正确做法：使用默认参数
def create_multipliers_correct():
    multipliers = []
    for i in range(3):
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

funcs_correct = create_multipliers_correct()
print(f"正确结果：{[f(2) for f in funcs_correct]}")  # [0, 2, 4]

# 15. 类型检查工具
print("\n=== 类型检查 ===")
print("""
使用 mypy 进行静态类型检查：

安装：
    pip install mypy

检查文件：
    mypy your_script.py

配置文件 mypy.ini：
    [mypy]
    python_version = 3.10
    warn_return_any = True
    warn_unused_configs = True
    disallow_untyped_defs = True
""")

print("\n命名空间、作用域与类型注解演示完成！")
