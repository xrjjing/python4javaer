"""
TODO 相关业务逻辑（Service 层）。

职责：
- 组合 Repository 操作与业务规则；
- 对外暴露与路由层对齐的高层接口。
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import todo_repository


def list_todos_for_user(db: Session, user: models.User) -> List[models.Todo]:
    """列出指定用户的所有 TODO。"""
    return todo_repository.list_todos_by_owner(db, owner_id=user.id)


def create_todo_for_user(
    db: Session,
    user: models.User,
    todo_in: schemas.TodoCreate,
) -> models.Todo:
    """为指定用户创建 TODO。"""
    return todo_repository.create_todo_for_owner(
        db=db,
        owner_id=user.id,
        title=todo_in.title,
        completed=todo_in.completed,
    )


def update_todo_for_user(
    db: Session,
    user: models.User,
    todo_id: int,
    todo_in: schemas.TodoUpdate,
) -> models.Todo:
    """
    更新指定用户的 TODO。

    若不存在或不属于该用户，抛出 ValueError 以由上层转换为 404。
    """
    todo = todo_repository.get_todo_by_id_for_owner(
        db=db,
        todo_id=todo_id,
        owner_id=user.id,
    )
    if not todo:
        raise ValueError("Todo 不存在或不属于当前用户")

    if todo_in.title is not None:
        todo.title = todo_in.title
    if todo_in.completed is not None:
        todo.completed = todo_in.completed

    return todo_repository.save_todo(db, todo)


def delete_todo_for_user(
    db: Session,
    user: models.User,
    todo_id: int,
) -> None:
    """
    删除指定用户的 TODO。

    若不存在或不属于该用户，抛出 ValueError 以由上层转换为 404。
    """
    todo = todo_repository.get_todo_by_id_for_owner(
        db=db,
        todo_id=todo_id,
        owner_id=user.id,
    )
    if not todo:
        raise ValueError("Todo 不存在或不属于当前用户")

    todo_repository.delete_todo(db, todo)


