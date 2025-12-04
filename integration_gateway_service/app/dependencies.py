"""
依赖注入相关工具。

包括：
- 获取通用后端服务客户端；
- 基于 RBAC 风格的 JWT 验证当前用户（简化版，只校验签名与基本字段）。
"""

from typing import Annotated, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from .client_backend_service import BackendServiceClient
from .log_detective_client import LogDetectiveClient
from .config import settings


http_bearer_scheme = HTTPBearer(auto_error=False)


def get_backend_client() -> BackendServiceClient:
    """注入通用后端服务客户端实例。"""
    return BackendServiceClient()


def get_log_detective_client() -> LogDetectiveClient:
    """注入日志侦探服务客户端实例。"""
    return LogDetectiveClient()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer_scheme)],
) -> Dict[str, Any]:
    """
    从 Authorization Bearer Token 中解析当前用户信息。

    这里假定 Token 由 RBAC 服务签发，并使用相同的 SECRET_KEY 与算法。
    仅做基础校验与 payload 解析，更复杂的权限控制仍建议由 RBAC 服务承担。
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少认证信息",
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.rbac_jwt_secret_key,
            algorithms=[settings.rbac_jwt_algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
        )

    # 这里保留 payload 的原始结构，方便调用方按需取出 sub/roles 等信息。
    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌中缺少用户标识字段",
        )
    return payload


CurrentUserPayload = Annotated[Dict[str, Any], Depends(get_current_user)]
