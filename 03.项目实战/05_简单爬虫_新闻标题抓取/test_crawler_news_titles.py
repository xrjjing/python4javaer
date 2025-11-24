"""crawler_news_titles 爬虫脚本中 HTML 解析逻辑的测试。"""

from pathlib import Path

import sys


def _import_crawler():
    """动态导入 crawler_news_titles 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import crawler_news_titles  # type: ignore

    return crawler_news_titles


def test_extract_titles_basic() -> None:
    """应能从 HTML 中提取长度足够的 <a> 文本。"""
    crawler = _import_crawler()

    html = """
    <html>
      <body>
        <a href="/1">短</a>
        <a href="/2">这是一个较长的标题</a>
        <a href="/3">另外一个新闻标题示例</a>
      </body>
    </html>
    """
    titles = crawler.extract_titles(html)

    # 短文本应被过滤掉
    assert all(len(t) >= 6 for t in titles)
    assert "这是一个较长的标题" in titles
    assert "另外一个新闻标题示例" in titles

