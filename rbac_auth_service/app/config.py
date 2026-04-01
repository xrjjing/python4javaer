"""
RBAC 服务配置模块。

职责：
- 统一管理数据库、Redis、JWT、审计日志服务地址；
- 给 database.py / security.py / log_audit_client.py 提供共享配置。

排查建议：
- 登录签名失败先看 secret_key；
- 黑名单不生效先看 redis_url；
- 审计日志不上报先看 log_audit_base_url。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import AnyUrl, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    全局配置对象。

    约定的环境变量包括（括号内为字段名）：
    - DATABASE_URL (database_url)
    - REDIS_URL (redis_url)
    - SECRET_KEY (secret_key)
    - ACCESS_TOKEN_EXPIRE_MINUTES (access_token_expire_minutes)
    """

    # 数据库连接字符串，默认使用当前目录下的 SQLite
    database_url: str = "sqlite:///./rbac.db"

    # Redis 连接字符串，未配置则不启用 Redis 版 Token 黑名单
    redis_url: Optional[str] = None

    # JWT 相关配置
    secret_key: str = "CHANGE_ME_TO_A_RANDOM_SECRET"
    access_token_expire_minutes: int = 60

    # 日志 / 审计服务基础地址，未配置则不上报审计日志
    log_audit_base_url: Optional[AnyHttpUrl] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    使用 lru_cache 缓存配置，避免重复解析环境变量。

    在应用中统一通过 get_settings() 获取配置实例：

        from .config import get_settings
        settings = get_settings()
    """

    return Settings()


settings = get_settings()


__all__ = ["Settings", "settings", "get_settings"]
