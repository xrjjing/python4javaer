"""示例爬虫：使用 requests + BeautifulSoup 抓取新闻标题。

设计要点：
- 默认读取本地样例 HTML（避免网络依赖），也可传入 URL 真实请求。
- 解析逻辑与网络层解耦，便于单测。
- 保留 User-Agent，遵守 robots 与站点条款（仅作教学示例）。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup


DEFAULT_SAMPLE = Path(__file__).parent / "sample_news.html"


@dataclass
class Article:
    title: str
    url: str | None = None


def fetch_html(url: str, timeout: int = 10) -> str:
    """从网络获取 HTML，演示用；生产环境需遵守 robots/授权。"""
    headers = {
        "User-Agent": "learn-spider/1.0 (+https://example.com)"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def parse_articles(html: str) -> List[Article]:
    """从 HTML 中提取文章标题与链接。"""
    soup = BeautifulSoup(html, "html.parser")
    results: List[Article] = []
    for a in soup.select("a.news-link"):
        title = (a.get_text() or "").strip()
        href = a.get("href")
        if title:
            results.append(Article(title=title, url=href))
    return results


def save_titles(articles: Iterable[Article], path: Path) -> None:
    path.write_text("\n".join(a.title for a in articles), encoding="utf-8")


def main() -> None:
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target.startswith("http"):
            html = fetch_html(target)
        else:
            html = Path(target).read_text(encoding="utf-8")
    else:
        html = DEFAULT_SAMPLE.read_text(encoding="utf-8")

    articles = parse_articles(html)
    print(f"共提取 {len(articles)} 条标题：")
    for art in articles:
        print(f"- {art.title} ({art.url or '无链接'})")

    out = Path("titles.txt")
    save_titles(articles, out)
    print(f"已写入 {out.resolve()}")


if __name__ == "__main__":
    main()
