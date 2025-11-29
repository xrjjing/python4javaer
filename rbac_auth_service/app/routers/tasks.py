"""
受 RBAC 控制的 Task 示例接口：
- 列表 / 创建 / 更新 / 删除
- 通过 require_permissions 控制访问权限
- 路径以项目为前缀：/projects/{project_id}/tasks
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_active_user, require_permissions
from ..services import task_service

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
)


@router.get(
    "/",
    response_model=schemas.APIResponse[List[schemas.TaskOut]],
    dependencies=[Depends(require_permissions("tasks:read"))],
)
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """列出当前用户某个项目下的任务。"""
    try:
        tasks = task_service.list_tasks_for_user_in_project(
            db=db,
            user=current_user,
            project_id=project_id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Project 不存在")
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="获取任务列表成功",
        data=tasks,
    )


@router.post(
    "/",
    response_model=schemas.APIResponse[schemas.TaskOut],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("tasks:write"))],
)
def create_task(
    project_id: int,
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """在当前用户指定的项目下创建任务。"""
    try:
        task = task_service.create_task_for_user_in_project(
            db=db,
            user=current_user,
            project_id=project_id,
            task_in=task_in,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Project 不存在")
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="创建任务成功",
        data=task,
    )


@router.put(
    "/{task_id}",
    response_model=schemas.APIResponse[schemas.TaskOut],
    dependencies=[Depends(require_permissions("tasks:write"))],
)
def update_task(
    project_id: int,
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """更新当前用户某个项目下的任务。"""
    try:
        task = task_service.update_task_for_user_in_project(
            db=db,
            user=current_user,
            project_id=project_id,
            task_id=task_id,
            task_in=task_in,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Task 不存在")
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="更新任务成功",
        data=task,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions("tasks:delete"))],
)
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """删除当前用户某个项目下的任务（需要 tasks:delete 权限）。"""
    try:
        task_service.delete_task_for_user_in_project(
            db=db,
            user=current_user,
            project_id=project_id,
            task_id=task_id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Task 不存在")
    return None

