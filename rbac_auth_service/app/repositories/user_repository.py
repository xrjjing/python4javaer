"""
用户相关持久化操作（Repository 层）。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """根据用户名获取用户。"""
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """根据 ID 获取用户。"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def list_users(db: Session) -> List[models.User]:
    """列出所有用户。"""
    return db.query(models.User).all()


def save_user(db: Session, user: models.User) -> models.User:
    """保存用户实体。"""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


