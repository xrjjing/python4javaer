"""网络客户端进阶示例（全部 Mock，脱网可运行）"""

from __future__ import annotations

import asyncio
import time
from urllib import request

import httpx


def demo_urllib():
    req = request.Request("https://example.com", method="GET")
    req.add_header("User-Agent", "learn-bot/1.0")
    # 不实际发网：只展示构造（避免沙箱限制）
    print("urllib request prepared:", req.full_url, req.get_header("User-Agent"))


def demo_httpx_sync():
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"ok": True, "path": str(r.url)}))
    with httpx.Client(timeout=5, transport=transport) as client:
        resp = client.get("https://api.test/mock")
        print("httpx sync:", resp.json())


async def demo_httpx_async():
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"async": True, "path": str(r.url)}))
    async with httpx.AsyncClient(timeout=5, transport=transport) as client:
        resp = await client.get("https://api.test/mock")
        print("httpx async:", resp.json())


def demo_retrying_client(retries: int = 2, backoff: float = 0.05):
    def send_with_retry(request_obj: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            # 首次返回 503，后续返回 200
            status = 503 if attempt == 0 else 200
            resp = httpx.Response(status, json={"attempt": attempt})
            if resp.status_code == 200 or attempt >= retries:
                return resp
            attempt += 1
            time.sleep(backoff * attempt)

    client = httpx.Client(timeout=5, transport=httpx.MockTransport(send_with_retry))
    resp = client.get("https://api.test/retry")
    print("retry client:", resp.json())
    client.close()


def main():
    demo_urllib()
    demo_httpx_sync()
    asyncio.run(demo_httpx_async())
    demo_retrying_client()


if __name__ == "__main__":
    main()
