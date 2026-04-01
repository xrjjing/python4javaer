"""
日志 / 审计服务数据库初始化与会话管理。

这个文件是数据层入口，主要负责：
- 创建 engine；
- 创建 SessionLocal；
- 提供 FastAPI 依赖 get_db()。

如果日志接口报数据库连接问题，通常先从这里查。
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from .config import settings


SQLALCHEMY_DATABASE_URL = settings.database_url

connect_args = (
    {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

# engine 是整个服务共享的数据库连接入口。
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# 每次请求通常会从这里拿一个独立 Session。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：获取一个数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
