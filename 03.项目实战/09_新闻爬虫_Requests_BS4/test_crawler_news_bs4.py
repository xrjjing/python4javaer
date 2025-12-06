from pathlib import Path

from crawler_news_bs4 import Article, parse_articles


def test_parse_articles_sample_html():
    html = (Path(__file__).parent / "sample_news.html").read_text(encoding="utf-8")
    articles = parse_articles(html)
    assert len(articles) == 3
    assert articles[0] == Article(title="Python 3.13 发布带来性能优化", url="https://news.example.com/1")
