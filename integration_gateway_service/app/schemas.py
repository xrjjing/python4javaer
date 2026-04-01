"""
网关服务使用到的 Pydantic 模型定义。

这份模型主要承担两类职责：
- 描述网关自己对外暴露的统一响应结构；
- 约束网关和下游 backend_user_order_service 之间共享的订单数据结构。

排查建议：
- 如果 router 返回成功但前端字段不对，先看 ApiResponse
- 如果 create_order 校验失败，先看 OrderCreateIn / OrderOut
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class OrderCreateIn(BaseModel):
    """创建订单入参模型，对应下游订单服务的创建接口。"""

    user_id: int = Field(..., description="下单用户 ID")
    product_id: int = Field(..., description="商品 ID")
    quantity: int = Field(..., ge=1, description="购买数量")


class OrderOut(BaseModel):
    """订单返回模型，对应下游订单服务返回的数据结构。"""

    order_id: int = Field(..., description="订单 ID")
    status: str = Field(..., description="订单状态")
    message: Optional[str] = Field(None, description="额外说明信息")
    created_at: datetime = Field(..., description="订单创建时间")


class ApiResponse(BaseModel):
    """统一 API 响应包装结构。"""

    success: bool = Field(..., description="请求是否成功")
    data: Optional[Any] = Field(None, description="返回数据载荷")
    error: Optional[str] = Field(None, description="错误信息")
