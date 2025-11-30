"""
对外网关路由定义。

该模块提供代理调用下游用户/订单服务的示例接口，并演示如何结合
RBAC 风格的认证与“由网关补充用户信息”的典型模式。
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies import get_backend_client, CurrentUserPayload
from ..schemas import ApiResponse, OrderCreateIn, OrderOut
from ..client_backend_service import BackendServiceClient, BackendServiceError
from ..log_audit_client import log_audit_client


router = APIRouter(prefix="/gateway", tags=["gateway"])


@router.get("/backend/users/{user_id}", response_model=ApiResponse)
def proxy_get_user(
    user_id: int,
    current_user: CurrentUserPayload,
    backend_client: BackendServiceClient = Depends(get_backend_client),
) -> ApiResponse:
    """
    代理调用下游用户服务的查询接口。

    仅作为示例：调用前会校验当前用户的身份，再转发请求。
    """
    # 这里可以根据 current_user 中的角色/权限做更细粒度控制，此处先只要求登录成功。
    try:
        user_data: Dict[str, Any] = backend_client.get_user(user_id)
    except BackendServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return ApiResponse(success=True, data=user_data)


@router.post("/backend/orders", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def proxy_create_order(
    order_in: OrderCreateIn,
    current_user: CurrentUserPayload,
    request: Request,
    backend_client: BackendServiceClient = Depends(get_backend_client),
) -> ApiResponse:
    """
    代理调用下游订单服务的创建订单接口。

    示例中会将当前用户 ID 写入下游请求，模拟“网关根据登录身份补充参数”的场景。
    """
    # 假定 payload 中的 sub 字段就是用户 ID。
    try:
        user_id = int(current_user["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前用户信息不完整，无法创建订单",
        )

    # 简单示例：只有超级管理员才允许通过网关创建订单
    is_superuser = bool(current_user.get("is_superuser"))
    if not is_superuser:
        client_host = request.client.host if request and request.client else None
        log_audit_client.send_log(
            {
                "actor": str(user_id),
                "action": "create_order_via_gateway_denied",
                "resource": "order",
                "source_service": "gateway",
                "ip": client_host,
                "detail": "普通用户尝试通过网关创建订单，被拒绝",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法创建订单",
        )

    enriched_order = OrderCreateIn(
        user_id=user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
    )

    try:
        order_out: OrderOut = backend_client.create_order(enriched_order)
    except BackendServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    # 上报通过网关创建订单的审计日志（失败时静默忽略）
    client_host = request.client.host if request.client else None
    log_audit_client.send_log(
        {
            "actor": str(user_id),
            "action": "create_order_via_gateway",
            "resource": "order",
            "source_service": "gateway",
            "ip": client_host,
            "detail": f"通过网关为用户 {user_id} 创建订单 {order_out.order_id}",
        }
    )

    return ApiResponse(success=True, data=order_out.dict())
