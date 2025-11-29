"""
受 RBAC 控制的 TODO 示例接口：
- 列表 / 创建 / 更新 / 删除
- 通过 require_permissions 控制访问权限
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_active_user, require_permissions
from ..services import todo_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get(
    "/",
    response_model=schemas.APIResponse[List[schemas.TodoOut]],
    dependencies=[Depends(require_permissions("todos:read"))],
)
def list_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """列出当前用户的 TODO。"""
    todos = todo_service.list_todos_for_user(db, current_user)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="获取 TODO 列表成功", data=todos
    )


@router.post(
    "/",
    response_model=schemas.APIResponse[schemas.TodoOut],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("todos:write"))],
)
def create_todo(
    todo_in: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """为当前用户创建 TODO。"""
    todo = todo_service.create_todo_for_user(db, current_user, todo_in)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="创建 TODO 成功", data=todo
    )


@router.put(
    "/{todo_id}",
    response_model=schemas.APIResponse[schemas.TodoOut],
    dependencies=[Depends(require_permissions("todos:write"))],
)
def update_todo(
    todo_id: int,
    todo_in: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """更新当前用户的 TODO。"""
    try:
        todo = todo_service.update_todo_for_user(
            db=db,
            user=current_user,
            todo_id=todo_id,
            todo_in=todo_in,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo 不存在")
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="更新 TODO 成功", data=todo
    )


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions("todos:delete"))],
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """删除当前用户的 TODO（需要 todos:delete 权限）。"""
    try:
        todo_service.delete_todo_for_user(
            db=db,
            user=current_user,
            todo_id=todo_id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo 不存在")
    # 无内容返回，统一响应结构交由前端自行处理或在中间件中封装
    return None

