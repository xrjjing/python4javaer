import sys
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup


def fetch_html(url: str, timeout: int = 10) -> str:
    """
    获取网页 HTML 内容。

    :param url: 目标网址
    :param timeout: 超时时间（秒）
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def extract_titles(html: str) -> List[str]:
    """
    从 HTML 中提取看起来像标题的文本。

    简化策略：
    - 遍历所有 <a> 标签；
    - 去掉前后空白；
    - 过滤掉太短的文本。
    """
    soup = BeautifulSoup(html, "html.parser")
    titles: List[str] = []
    for a in soup.find_all("a"):
        text = (a.get_text() or "").strip()
        if len(text) >= 6:
            titles.append(text)
    # 去重保持顺序
    seen = set()
    unique_titles: List[str] = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            unique_titles.append(t)
    return unique_titles


def save_titles(titles: Iterable[str], path: Path) -> None:
    """将标题写入文本文件。"""
    with path.open("w", encoding="utf-8") as f:
        for t in titles:
            f.write(t + "\n")


def main() -> None:
    if len(sys.argv) < 2:
        print("用法：python crawler_news_titles.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"正在抓取：{url}")
    html = fetch_html(url)
    titles = extract_titles(html)

    print(f"共提取到 {len(titles)} 条候选标题：")
    for t in titles[:30]:
        print("-", t)
    if len(titles) > 30:
        print("...（仅显示前 30 条）")

    out_path = Path("titles.txt")
    save_titles(titles, out_path)
    print(f"已将全部标题写入：{out_path.resolve()}")


if __name__ == "__main__":
    main()

