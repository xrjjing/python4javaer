# asyncio 进阶：gather/超时/取消

## 1. 并发执行：asyncio.gather

```python
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    return name, delay

async def main():
    results = await asyncio.gather(
        task("A", 0.2),
        task("B", 0.1),
        task("C", 0.3),
    )
    print(results)

asyncio.run(main())
```

## 2. 超时控制：asyncio.wait_for

```python
async def slow():
    await asyncio.sleep(1)

asyncio.run(asyncio.wait_for(slow(), timeout=0.2))
```

若超时会抛出 `TimeoutError`，可在上层捕获并降级。

## 3. 取消任务：task.cancel()

```python
async def cancellable():
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("task cancelled")
        raise

async def main():
    t = asyncio.create_task(cancellable())
    await asyncio.sleep(0.1)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("handled cancel")

asyncio.run(main())
```

## 4. 何时用 gather vs as_completed
- 需要所有任务结果、失败即抛：`gather`
- 需最快结果或流式消费：`as_completed`

## 5. 与本仓库的联系
- 网关/日志侦探可用 `asyncio.wait_for` 为下游调用设定超时并返回 504。
- 批处理或爬虫可用 `gather` 并发请求并汇总结果。

## 6. 配套示例
- 运行：`python 01.Python语言基础/15_进阶专题/07_异步编程入门/demo_asyncio_adv.py`
