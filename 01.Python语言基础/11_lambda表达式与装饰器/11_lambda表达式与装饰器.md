# 11_lambda 表达式与装饰器

> 本章偏「基础进阶」，在语法上不是必须，但在实际开发中非常常见，建议在前面章节较熟练后再学习。

## 学习目标

- 理解 `lambda` 表达式的基本语法与适用场景
- 初步理解装饰器（decorator）的概念和作用
- 能编写简单的函数装饰器，例如统计执行时间、打印日志

---

## 知识点清单

### 1. lambda 表达式

- 语法：`lambda 参数列表: 表达式`
- 适用场景：需要一个「小函数」且只在局部使用，例如排序 key、回调等。

```python
nums = [3, 1, 5, 2]
nums_sorted = sorted(nums, key=lambda x: -x)  # 按降序排序
```

### 2. 装饰器的概念

- 本质：一个「接收函数并返回新函数」的高阶函数，用来在不修改原函数代码的前提下，增加额外功能（如打印日志、权限校验、缓存等）。

基本形式：

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result

    return wrapper


@my_decorator
def say_hi():
    print("Hi")
```

---

## 示例 demo：记录函数执行时间的装饰器

```python
# demo_lambda_decorator.py

import time
from typing import Callable, Any


def timeit(func: Callable) -> Callable:
    """简单的计时装饰器"""

    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 执行耗时：{end - start:.6f} 秒")
        return result

    return wrapper


@timeit
def slow_add(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


if __name__ == "__main__":
    # lambda 示例：筛选偶数
    nums = [1, 2, 3, 4, 5, 6]
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print("偶数列表：", evens)

    # 装饰器示例
    result = slow_add(1_000_00)
    print("结果：", result)
```

---

## 练习题（建议新建 `practice_lambda_decorator.py` 完成）

1. 使用 `lambda` 表达式，对一个字符串列表按长度排序，例如：`["python", "java", "c"]`。  
2. 使用 `lambda` 和 `map`，把一个整数列表中的每个元素都平方。  
3. 编写一个装饰器 `log_call`，在函数调用前后打印：  
   - 函数名  
   - 传入的参数  
   用它装饰一个简单的求和函数并测试。  
4. 思考题：如果一个函数已经被装饰器包装过，再给它加另一个装饰器会发生什么？你能写一段代码验证你的猜想吗？

