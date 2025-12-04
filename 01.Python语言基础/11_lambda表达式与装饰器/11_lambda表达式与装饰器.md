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

---

## 🎯 开放式挑战

### 挑战 1：智能缓存装饰器（中级）

**任务描述**：
实现一个带过期时间的缓存装饰器，自动缓存函数的计算结果。

**功能需求**：
```python
@cache(ttl=60)  # 缓存 60 秒
def expensive_computation(n):
    time.sleep(2)  # 模拟耗时计算
    return sum(range(n))

# 第一次调用：耗时 2 秒
result1 = expensive_computation(1000000)

# 第二次调用（60 秒内）：立即返回（从缓存）
result2 = expensive_computation(1000000)

# 60 秒后再调用：重新计算
```

**技术要点**：
- 使用字典存储缓存：`{参数: (结果, 过期时间)}`
- 使用 `functools.wraps` 保留原函数元数据
- 处理可变参数（`*args, **kwargs`）
- 使用 `time.time()` 检查缓存是否过期

**扩展功能**：
- 支持最大缓存数量（LRU 策略）
- 缓存命中率统计
- 支持清空缓存的方法

**提示**：
参考 `functools.lru_cache` 的设计思路

---

### 挑战 2：API 限流装饰器（高级）

**任务描述**：
实现一个限流装饰器，控制函数的调用频率（用于 API 接口保护）。

**使用示例**：
```python
@rate_limit(max_calls=5, period=60)
def call_third_party_api(user_id):
    # 调用外部 API
    return requests.get(f"https://api.example.com/users/{user_id}")

# 前 5 次调用正常
for i in range(5):
    call_third_party_api(123)  # 成功

# 第 6 次调用：抛出 RateLimitExceeded 异常
call_third_party_api(123)  # 失败
```

**技术挑战**：
1. **滑动窗口算法**
   - 记录每次调用的时间戳
   - 清理过期的时间戳
   - 判断当前时间窗口内的调用次数

2. **线程安全**
   - 使用 `threading.Lock` 保护共享数据
   - 处理并发调用的竞态条件

3. **区分不同参数**
   ```python
   @rate_limit(max_calls=3, period=60, per_user=True)
   def send_email(user_id, message):
       # 每个用户独立限流
       pass
   ```

**核心数据结构**：
```python
call_history = {
    'func_name': [timestamp1, timestamp2, ...],
    'func_name:user_123': [timestamp1, ...]  # 基于参数的限流
}
```

**扩展功能**：
- 支持自定义限流策略（令牌桶、漏桶）
- 返回剩余调用次数
- 集成 Redis 实现分布式限流

---

### 挑战 3：性能分析装饰器组合（综合实战）

**任务描述**：
设计一套可组合的性能分析装饰器，用于监控函数执行情况。

**装饰器套件**：
```python
@retry(max_attempts=3, delay=1)  # 失败重试
@timeout(seconds=5)              # 超时控制
@measure_time                    # 耗时统计
@log_calls                       # 调用日志
def unreliable_api_call(url):
    response = requests.get(url)
    return response.json()
```

**各装饰器功能**：

1. **`@retry`**：失败自动重试
   - 捕获指定异常
   - 指数退避（delay * 2^attempt）
   - 记录重试次数

2. **`@timeout`**：超时控制
   - 使用 `signal`（Linux）或 `threading.Timer`（跨平台）
   - 超时抛出 `TimeoutError`

3. **`@measure_time`**：性能统计
   - 记录函数执行时间
   - 计算平均耗时、最大/最小耗时
   - 生成性能报告

4. **`@log_calls`**：调用追踪
   - 记录参数、返回值、异常
   - 支持日志级别配置
   - 集成 logging 模块

**技术要点**：
- 装饰器链的顺序很重要（内层到外层）
- 使用 `functools.wraps` 保留函数签名
- 异常传播与处理
- 上下文管理器（`with` 语句）配合使用

**预期输出**：
```
[2025-01-15 10:00:00] INFO: Calling unreliable_api_call(url='https://...')
[2025-01-15 10:00:01] WARNING: Attempt 1 failed, retrying in 1s...
[2025-01-15 10:00:03] WARNING: Attempt 2 failed, retrying in 2s...
[2025-01-15 10:00:06] INFO: Call succeeded after 3 attempts
[2025-01-15 10:00:06] INFO: Execution time: 6.2s
```

**评估标准**：
- 装饰器可独立使用也可组合使用
- 异常处理完善
- 代码复用性高（DRY 原则）
- 性能开销小

