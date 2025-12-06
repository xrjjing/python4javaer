# 面向对象高级特性速览

> 结合 Java 经验，聚焦 Python 中常用的 OOP 进阶特性与差异点。配套代码：`demo_oop_advanced.py`。

## 1. 属性控制：@property

```python
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius  # 会调用 setter 做校验

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value
```

要点：
- 与 Java getter/setter 不同，Python 用装饰器即可实现属性访问控制，调用端依旧是 `obj.celsius`。
- 可搭配 `@property` 提供只读派生属性（如 `kelvin`）。

## 2. 内存与字段限制：__slots__

```python
class Vector2D:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

要点：
- 限定可用属性，阻止意外新增字段，节省内存（大量实例时收益明显）。
- 注意：__slots__ 类不能再随意添加新属性；与多继承一起使用时需小心（子类也要定义 __slots__）。

## 3. 可迭代/下标访问：__iter__、__len__、__getitem__

```python
class Vector2D:
    def __iter__(self):
        yield from (self.x, self.y)
    def __len__(self):
        return 2
    def __getitem__(self, index):
        return (self.x, self.y)[index]
```

要点：
- 让自定义对象表现得像序列：可用于解包、for 循环、len()、切片等。
- 与 Java 的 Iterable 接口类似，但通过魔术方法直接定制。

## 4. 多重继承与 MRO

```python
class LoggerMixin:
    def log(self, msg): print(f"[LOG] {msg}")

class AuditMixin:
    def audit(self, msg): print(f"[AUDIT] {msg}")

class Service(LoggerMixin, AuditMixin):
    pass
```

要点：
- Python 采用 C3 线性化计算方法解析方法解析顺序（MRO）：`Service.__mro__`
- Mixins 场景常见，注意避免菱形继承的冲突，必要时显式调用 `super()`

## 5. 元类（Metaclass）示例：单例

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    pass
```

要点：
- 元类控制“创建类的过程”，可用于注入单例、自动注册等高级场景。
- 仅在确有需求时使用；大多数业务场景用装饰器/工厂已足够。

## 6. 参考与实践
- 运行示例：`python 01.Python语言基础/09_面向对象入门/demo_oop_advanced.py`
- 结合本仓库：RBAC、网关服务中大量使用依赖注入和类封装，可观察 Pydantic / SQLAlchemy 对象的属性行为。
- 对照廖雪峰教程章节：面向对象高级编程（slots/property/多重继承/定制类/元类）。
