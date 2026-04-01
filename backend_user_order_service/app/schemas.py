"""
后端用户与订单服务的 Pydantic 模型定义。

作用：
- 定义下游服务自己的输入输出结构；
- 同时作为 integration_gateway_service 校验下游返回数据的参照。

排查建议：
- 如果网关提示“返回数据结构不符合预期”，先对照这里看字段名和类型。
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
