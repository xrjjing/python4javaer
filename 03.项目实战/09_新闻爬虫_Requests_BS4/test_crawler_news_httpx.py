import asyncio
from pathlib import Path

import httpx

from crawler_news_httpx import Article, parse_articles


def test_async_parser_with_local_html():
    html = (Path(__file__).parent / "sample_news.html").read_text(encoding="utf-8")
    articles = parse_articles(html)
    assert len(articles) == 3
    assert articles[1] == Article(
        title="FastAPI 入门教程：从零到部署", url="https://news.example.com/2"
    )


def test_rate_limiter_mock_request():
    async def run():
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200, text="<a class='news-link'>Mock Title</a>"
            )

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            resp = await client.get("https://api.test/mock")
            assert resp.status_code == 200

    asyncio.run(run())


def test_rate_limiter_backoff():
    from crawler_news_httpx import RateLimiter

    limiter = RateLimiter(rps=2.0)
    limiter.backoff()
    assert 0.19 < limiter.rps < 2.0


def test_allowed_by_robots_false(monkeypatch):
    from crawler_news_httpx import allowed_by_robots
    import crawler_news_httpx as mod

    class FakeRP:
        def set_url(self, url):
            self.url = url

        def read(self):
            return True

        def can_fetch(self, ua, url):
            return False

    monkeypatch.setattr(mod.robotparser, "RobotFileParser", lambda: FakeRP())
    assert allowed_by_robots("https://example.com/blocked") is False
