# app/deps.py
"""
依赖注入：组装依赖链
依赖链完整路径：Settings → Engine → Session → Repository → Route
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from .db import get_session
from .repositories import UserRepository


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    """
    获取用户仓储
    Java 对比：@Autowired UserRepository

    依赖链：get_settings → get_engine → get_session → get_user_repo
    """
    return UserRepository(session)
