"""
RBAC 服务数据库入口。

职责：
- 创建 SQLAlchemy engine / SessionLocal / Base；
- 对外提供 get_db() 依赖，供 routers / services / repositories 统一使用。

排查建议：
- 表没创建、连接串不对、Session 异常时，优先从这里开始。
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
