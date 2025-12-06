"""基于 fakeredis 的内存 Redis，用于离线测试。"""

try:
    import fakeredis  # type: ignore
except ImportError:  # pragma: no cover
    fakeredis = None


def get_fake_redis():
    """返回一个 fakeredis.Redis 实例，若未安装则抛出明确提示。"""
    if fakeredis is None:
        raise RuntimeError("fakeredis 未安装，无法创建内存 Redis。请先 pip install fakeredis")
    return fakeredis.FakeRedis()
