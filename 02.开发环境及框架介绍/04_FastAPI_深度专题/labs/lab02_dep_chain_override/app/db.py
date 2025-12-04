# app/db.py
"""
数据库连接管理：依赖链的中间环节
依赖链：Settings → Engine → Session
Java 对比：DataSource → EntityManagerFactory → EntityManager
"""
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

from .config import Settings, get_settings

# 全局 Engine 缓存（避免每请求创建）
_engine_cache: dict[str, Engine] = {}


def get_engine(settings: Settings = Depends(get_settings)) -> Engine:
    """
    获取数据库引擎
    Java 对比：DataSource Bean
    """
    if settings.database_url not in _engine_cache:
        engine = create_engine(
            settings.database_url,
            echo=settings.echo_sql,
            future=True,
            # SQLite 需要此参数支持多线程
            connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
        )
        _engine_cache[settings.database_url] = engine
    return _engine_cache[settings.database_url]


def get_session(engine: Engine = Depends(get_engine)) -> Generator[Session, None, None]:
    """
    获取数据库会话（请求级生命周期）
    Java 对比：@RequestScope EntityManager

    依赖链：get_settings → get_engine → get_session
    """
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
