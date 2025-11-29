"""
数据库配置与 Session 管理。

默认使用 SQLite，便于快速上手；
在实际环境中可以通过环境变量切换到 MySQL。
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖注入使用的数据库会话生成器。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
