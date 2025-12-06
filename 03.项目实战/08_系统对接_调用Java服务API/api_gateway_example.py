from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

from client_java_service import JavaServiceClient, JavaServiceError


class OrderCreateIn(BaseModel):
    """Python 网关接收的订单创建请求体。"""

    user_id: int
    amount: float
    comment: Optional[str] = None


class OrderOut(BaseModel):
    """返回给调用方的订单信息（简化版）。"""

    id: int
    user_id: int
    amount: float


class ApiResponse(BaseModel):
    """
    通用网关响应模板。

    约定：
    - code: 业务状态码，0 表示成功，其它值可按需要自定义；
    - message: 对应的提示信息；
    - data: 具体业务数据（可以是字典、列表或具体模型的 .dict()）。

    说明：
    - 本示例中，为了简化起见，错误场景仍然通过 HTTP 4xx/5xx + detail 返回，
      ApiResponse 主要用于「成功响应」时统一格式。
    """

    code: int = 0
    message: str = "ok"
    data: Any | None = None


def get_java_client() -> JavaServiceClient:
    """FastAPI 依赖注入：获取 Java 服务客户端实例。"""
    return JavaServiceClient.from_env()


app = FastAPI(title="Python 网关示例（调用 Java 服务）")


@app.get("/proxy/users/{user_id}", response_model=ApiResponse)
def proxy_get_user(
    user_id: int,
    client: JavaServiceClient = Depends(get_java_client),
) -> ApiResponse:
    """
    代理查询用户信息。

    成功时：
    - 返回 ApiResponse，data 字段中包含来自 Java 服务的用户信息字典。

    失败时：
    - 将 JavaServiceError 转换为 HTTP 502，响应体为 FastAPI 默认的
      {"detail": "..."} 结构。
    """
    try:
        user_data = client.get_user(user_id)
    except JavaServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    return ApiResponse(code=0, message="ok", data=user_data)


@app.post("/proxy/orders", response_model=ApiResponse)
def proxy_create_order(
    order_in: OrderCreateIn,
    client: JavaServiceClient = Depends(get_java_client),
) -> ApiResponse:
    """
    代理创建订单，将外部接口包装成统一风格。

    成功时：
    - data 字段中返回经过 OrderOut 校验和转换后的订单信息。

    失败时：
    - JavaServiceError → HTTP 502；
    - Java 返回格式异常 → HTTP 500。
    """
    try:
        data = client.create_order(
            user_id=order_in.user_id,
            amount=order_in.amount,
            comment=order_in.comment,
        )
    except JavaServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    # 假设 Java 返回的数据中字段名为 id / userId / amount
    try:
        order = OrderOut(
            id=int(data["id"]),
            user_id=int(data.get("userId", order_in.user_id)),
            amount=float(data.get("amount", order_in.amount)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="订单接口返回格式异常",
        ) from exc

    return ApiResponse(code=0, message="ok", data=order.model_dump())
