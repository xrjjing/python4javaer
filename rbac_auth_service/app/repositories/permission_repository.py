"""
权限相关持久化操作（Repository 层）。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def get_permission_by_code(db: Session, code: str) -> Optional[models.Permission]:
    """根据权限 code 获取权限。"""
    return (
        db.query(models.Permission)
        .filter(models.Permission.code == code)
        .first()
    )


def get_permission_by_id(db: Session, perm_id: int) -> Optional[models.Permission]:
    """根据 ID 获取权限。"""
    return (
        db.query(models.Permission)
        .filter(models.Permission.id == perm_id)
        .first()
    )


def list_permissions(db: Session) -> List[models.Permission]:
    """列出所有权限。"""
    return db.query(models.Permission).all()


def save_permission(db: Session, perm: models.Permission) -> models.Permission:
    """保存权限实体。"""
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


