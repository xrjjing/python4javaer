"""
日志 / 审计服务数据库初始化与会话管理。
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from .config import settings


SQLALCHEMY_DATABASE_URL = settings.database_url

connect_args = (
    {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：获取一个数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

