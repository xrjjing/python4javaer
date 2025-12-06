"""
异步新闻爬虫示例：httpx + asyncio + 简单速率控制 + robots 检查

特点：
- 默认使用本地 sample_html（与同步版保持离线能力）
- 可传 URL 真实抓取，遵守 robots.txt；若 robots 禁止则拒绝抓取
- 简单 RateLimiter：初始 2 req/s，遇到 429/503 自动退避
"""

from __future__ import annotations

import asyncio
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib import robotparser

import httpx
from bs4 import BeautifulSoup


DEFAULT_SAMPLE = Path(__file__).parent / "sample_news.html"


@dataclass
class Article:
    title: str
    url: Optional[str] = None


class RateLimiter:
    def __init__(self, rps: float = 2.0):
        self.rps = rps
        self._last = 0.0

    async def wait(self):
        now = time.monotonic()
        gap = 1 / self.rps
        if now - self._last < gap:
            await asyncio.sleep(gap - (now - self._last))
        self._last = time.monotonic()

    def backoff(self):
        self.rps = max(0.2, self.rps * 0.5)


async def fetch_html(url: str, client: httpx.AsyncClient, limiter: RateLimiter) -> str:
    await limiter.wait()
    resp = await client.get(url, headers={"User-Agent": "learn-spider/1.0"}, follow_redirects=True)
    if resp.status_code in (429, 503):
        limiter.backoff()
    resp.raise_for_status()
    resp.encoding = resp.charset_encoding or resp.apparent_encoding
    return resp.text


def allowed_by_robots(url: str, ua: str = "learn-spider"):
    rp = robotparser.RobotFileParser()
    robots_url = str(httpx.URL(url).copy_with(path="/robots.txt"))
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        return True  # 读取失败时宽容处理
    return rp.can_fetch(ua, url)


def parse_articles(html: str) -> List[Article]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[Article] = []
    for a in soup.select("a.news-link"):
        title = (a.get_text() or "").strip()
        href = a.get("href")
        if title:
            results.append(Article(title=title, url=href))
    return results


async def main():
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        url = sys.argv[1]
        if not allowed_by_robots(url):
            print("robots.txt 禁止抓取该路径，已退出。")
            return
        limiter = RateLimiter(rps=2.0)
        async with httpx.AsyncClient(timeout=10) as client:
            html = await fetch_html(url, client, limiter)
    else:
        html = DEFAULT_SAMPLE.read_text(encoding="utf-8")

    articles = parse_articles(html)
    print(f"共提取 {len(articles)} 条标题：")
    for art in articles:
        print(f"- {art.title} ({art.url or '无链接'})")


if __name__ == "__main__":
    asyncio.run(main())
