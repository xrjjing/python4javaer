"""
TODO 业务服务层。

职责：
- 对 TODO 资源执行 owner 维度的读写控制；
- 把 repository 操作和“是否属于当前用户”这类规则封装起来。

上游：todos.py
下游：todo_repository.py
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


