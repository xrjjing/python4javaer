"""
认证与安全相关工具：
- 密码哈希与校验（使用 passlib[bcrypt]）
- JWT 的生成与验证
- 可选的 Redis Token 黑名单支持
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Optional

import jwt
from passlib.context import CryptContext

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover
    redis = None  # 如果未安装 redis，相关功能将被禁用

from .config import settings
from .schemas import TokenPayload


# ========== 密码哈希 ==========

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """对明文密码进行哈希。"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码与哈希是否匹配。"""
    return pwd_context.verify(plain_password, hashed_password)


# ========== JWT 配置 ==========

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(
    subject: int,
    username: str,
    is_superuser: bool,
    expires_minutes: int | None = None,
) -> str:
    """
    创建访问令牌（JWT）。

    :param subject: 用户 ID
    :param username: 用户名
    :param is_superuser: 是否超级管理员
    :param expires_minutes: 过期时间（分钟）
    """
    if expires_minutes is None:
        expires_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    now = int(time.time())
    expire = now + expires_minutes * 60
    jti = str(uuid.uuid4())

    to_encode: dict[str, Any] = {
        "sub": subject,
        "username": username,
        "is_superuser": is_superuser,
        "exp": expire,
        "iat": now,
        "jti": jti,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    """
    解析并验证 JWT，返回 TokenPayload。

    若验证失败抛出 jwt.PyJWTError 异常。
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return TokenPayload(**payload)


# ========== Redis 支持（Token 黑名单，可选） ==========


class TokenBlacklist:
    """
    Token 黑名单实现。

    - 如果配置了 REDIS_URL 且安装了 redis 库，则使用 Redis 存储；
    - 否则退化为进程内 set，仅适合本地单进程演示。
    """

    def __init__(self) -> None:
        self._backend = None
        self._memory_set: set[str] = set()

        redis_url = settings.redis_url
        if redis_url and redis is not None:
            try:
                self._backend = redis.Redis.from_url(redis_url)  # type: ignore[arg-type]
            except Exception:  # pragma: no cover - 连接失败时退化
                self._backend = None

    def add(self, jti: str, exp: int) -> None:
        """
        将 Token 的 jti 加入黑名单，直到过期时间。
        """
        ttl = max(0, exp - int(time.time()))
        if self._backend is not None:
            key = f"rbac:jwt:blacklist:{jti}"
            try:
                self._backend.set(key, "1", ex=ttl or None)
            except Exception:  # pragma: no cover
                # 出现故障时不阻止主流程，只记录在内存中
                self._memory_set.add(jti)
        else:
            self._memory_set.add(jti)

    def contains(self, jti: str) -> bool:
        """检查 jti 是否在黑名单中。"""
        if self._backend is not None:
            key = f"rbac:jwt:blacklist:{jti}"
            try:
                if self._backend.exists(key):
                    return True
            except Exception:  # pragma: no cover
                pass
        return jti in self._memory_set


token_blacklist = TokenBlacklist()


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "token_blacklist",
]
