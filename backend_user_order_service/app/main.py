"""
后端用户与订单示例服务入口。

运行示例（建议使用 9000 端口，以配合网关默认配置）：
    uvicorn backend_user_order_service.app.main:app --reload --port 9000
"""

from datetime import datetime
from itertools import count
from typing import Dict

from fastapi import FastAPI, HTTPException, status

from .schemas import OrderCreateIn, OrderOut, UserOut


app = FastAPI(title="Backend User & Order Service", version="0.1.0")


_user_store: Dict[int, UserOut] = {
    1: UserOut(id=1, username="alice", full_name="Alice Zhang"),
    2: UserOut(id=2, username="bob", full_name="Bob Li"),
}

_order_id_counter = count(start=1)


@app.get("/api/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    """
    根据用户 ID 查询用户信息。

    这里使用内存字典模拟用户数据，实际项目中可以替换为数据库查询。
    """
    user = _user_store.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return user


@app.post("/api/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreateIn) -> OrderOut:
    """
    创建订单并返回订单信息。

    为简化示例，这里不做持久化，仅生成自增 ID 并立即返回。
    """
    order_id = next(_order_id_counter)
    return OrderOut(
        order_id=order_id,
        status="CREATED",
        message=f"用户 {order_in.user_id} 创建了商品 {order_in.product_id} 的订单（数量：{order_in.quantity}）",
        created_at=datetime.utcnow(),
    )

