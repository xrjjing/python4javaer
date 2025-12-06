"""
面向对象高级示例：
- @property 读写控制与派生属性
- __slots__ 限定字段、节省内存
- __iter__ / __getitem__ / __len__ 让对象像序列
- 简单元类实现单例
"""

from __future__ import annotations

from math import hypot
from typing import Iterator


class Temperature:
    """演示 @property 校验与派生属性"""

    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15


class Vector2D:
    """__slots__ + 可迭代/下标访问 + 只读长度属性"""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[float]:
        yield from (self.x, self.y)

    def __len__(self) -> int:  # 允许 len(v)
        return 2

    def __getitem__(self, index: int) -> float:
        return (self.x, self.y)[index]

    @property
    def length(self) -> float:
        """向量长度，示范只读派生属性"""
        return hypot(self.x, self.y)

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})"


class SingletonMeta(type):
    """最小化单例元类实现"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """使用元类的配置单例"""

    def __init__(self):
        self.values = {}

    def set(self, key: str, value):
        self.values[key] = value

    def get(self, key: str, default=None):
        return self.values.get(key, default)


if __name__ == "__main__":
    print("=== property 示例 ===")
    t = Temperature(25)
    print("摄氏度:", t.celsius, "开尔文:", t.kelvin)
    try:
        t.celsius = -300
    except ValueError as exc:
        print("校验触发:", exc)

    print("\n=== __slots__ + 可迭代 ===")
    v = Vector2D(3, 4)
    print("向量:", v, "长度:", v.length)
    print("len(v):", len(v), "迭代展开:", list(v), "下标访问 v[0]:", v[0])

    print("\n=== 元类单例 ===")
    c1 = Config()
    c2 = Config()
    c1.set("env", "dev")
    print("同一实例?", c1 is c2, "值:", c2.get("env"))
