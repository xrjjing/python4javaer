"""asyncio 进阶示例：gather / wait_for / cancel"""

from __future__ import annotations

import asyncio


async def task(name: str, delay: float):
    await asyncio.sleep(delay)
    return name, delay


async def demo_gather():
    results = await asyncio.gather(
        task("A", 0.2),
        task("B", 0.1),
        task("C", 0.3),
    )
    print("gather results:", results)


async def demo_timeout():
    async def slow():
        await asyncio.sleep(1)

    try:
        await asyncio.wait_for(slow(), timeout=0.2)
    except asyncio.TimeoutError:
        print("timeout hit, downgraded")


async def demo_cancel():
    async def cancellable():
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("task cancelled")
            raise

    t = asyncio.create_task(cancellable())
    await asyncio.sleep(0.1)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("handled cancel")


async def main():
    await demo_gather()
    await demo_timeout()
    await demo_cancel()


if __name__ == "__main__":
    asyncio.run(main())
