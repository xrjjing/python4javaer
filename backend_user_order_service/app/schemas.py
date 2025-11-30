"""
后端用户与订单服务的 Pydantic 模型定义。
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    """用户信息返回模型。"""

    id: int = Field(..., description="用户 ID")
    username: str = Field(..., description="用户名")
    full_name: Optional[str] = Field(None, description="用户全名")


class OrderCreateIn(BaseModel):
    """创建订单入参模型。"""

    user_id: int = Field(..., description="下单用户 ID")
    product_id: int = Field(..., description="商品 ID")
    quantity: int = Field(..., ge=1, description="购买数量")


class OrderOut(BaseModel):
    """订单返回模型。"""

    order_id: int = Field(..., description="订单 ID")
    status: str = Field(..., description="订单状态")
    message: Optional[str] = Field(None, description="额外说明信息")
    created_at: datetime = Field(..., description="订单创建时间")

