"""
Pydantic 模型定义：请求与响应体。
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


# ===== 用户相关 =====


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    is_superuser: bool = False


class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class RoleSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PermissionSimple(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    is_superuser: bool
    roles: List[RoleSimple] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ===== 角色与权限 =====


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None


class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[PermissionSimple] = []

    class Config:
        orm_mode = True


class PermissionCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class PermissionOut(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class AssignRolesRequest(BaseModel):
    role_ids: List[int]


class AssignPermissionsRequest(BaseModel):
    permission_ids: List[int]


# ===== TODO 相关 =====


class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    owner_id: int

    class Config:
        orm_mode = True


# ===== Project 相关 =====


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ===== Task 相关 =====


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="todo", max_length=20)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ===== 认证相关 =====


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    username: str
    is_superuser: bool = False
    exp: int
    jti: str


class LoginRequest(BaseModel):
    username: str
    password: str


# ===== 统一响应与错误码 =====


class ErrorCode(str, Enum):
    """错误码与通用状态码枚举。"""

    OK = "OK"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class APIResponse(BaseModel, Generic[T]):
    """
    统一响应模型：
    - code: 业务或通用错误码
    - message: 文本描述
    - data: 具体数据载荷
    """

    code: ErrorCode
    message: str
    data: Optional[T] = None


__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "RoleCreate",
    "RoleOut",
    "PermissionCreate",
    "PermissionOut",
    "AssignRolesRequest",
    "AssignPermissionsRequest",
    "TodoCreate",
    "TodoUpdate",
    "TodoOut",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectOut",
    "TaskCreate",
    "TaskUpdate",
    "TaskOut",
    "Token",
    "TokenPayload",
    "LoginRequest",
    "ErrorCode",
    "APIResponse",
]
