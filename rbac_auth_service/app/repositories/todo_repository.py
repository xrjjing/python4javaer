"""
TODO 相关的持久化操作（Repository 层）。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def list_todos_by_owner(db: Session, owner_id: int) -> List[models.Todo]:
    """查询指定用户的全部 TODO。"""
    return (
        db.query(models.Todo)
        .filter(models.Todo.owner_id == owner_id)
        .all()
    )


def get_todo_by_id_for_owner(
    db: Session,
    todo_id: int,
    owner_id: int,
) -> Optional[models.Todo]:
    """根据 ID 查询 TODO，且确保属于指定用户。"""
    return (
        db.query(models.Todo)
        .filter(
            models.Todo.id == todo_id,
            models.Todo.owner_id == owner_id,
        )
        .first()
    )


def create_todo_for_owner(
    db: Session,
    owner_id: int,
    title: str,
    completed: bool = False,
) -> models.Todo:
    """为指定用户创建 TODO。"""
    todo = models.Todo(
        title=title,
        completed=completed,
        owner_id=owner_id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def save_todo(db: Session, todo: models.Todo) -> models.Todo:
    """保存已修改的 TODO。"""
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: models.Todo) -> None:
    """删除指定 TODO。"""
    db.delete(todo)
    db.commit()

