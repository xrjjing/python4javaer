"""
日志 / 审计服务用到的 Pydantic 模型定义。
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    """创建审计日志请求体。"""

    actor: Optional[str] = Field(None, description="触发操作的主体标识，例如用户ID或用户名")
    action: str = Field(..., description="执行的操作名称，例如 login/create_order")
    resource: Optional[str] = Field(None, description="被操作的资源名称，例如 user/order")
    source_service: Optional[str] = Field(
        None, description="来源服务名称，例如 rbac/gateway/backend"
    )
    ip: Optional[str] = Field(None, description="请求来源 IP 地址")
    detail: Optional[str] = Field(None, description="附加详情信息，通常为简要描述或上下文")


class AuditLogRead(BaseModel):
    """审计日志返回模型。"""

    id: int = Field(..., description="日志 ID")
    created_at: datetime = Field(..., description="日志创建时间（UTC）")
    actor: Optional[str] = Field(None, description="触发操作的主体标识")
    action: str = Field(..., description="执行的操作名称")
    resource: Optional[str] = Field(None, description="被操作的资源名称")
    source_service: Optional[str] = Field(None, description="来源服务名称")
    ip: Optional[str] = Field(None, description="请求来源 IP 地址")
    detail: Optional[str] = Field(None, description="附加详情信息")

    class Config:
        orm_mode = True

