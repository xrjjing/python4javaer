"""
网关服务配置模块。

通过配置类统一管理环境变量，支持从 .env 文件加载。
本模块不关心下游服务是用什么语言实现的，只负责提供统一的 HTTP
后端服务基础地址等配置，适合 Python 风格的微服务网关。
"""

from functools import lru_cache
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """网关服务配置类。"""

    backend_service_base_url: AnyHttpUrl = "http://localhost:9000"
    """下游 HTTP 后端服务基础地址，例如 http://localhost:9000"""

    rbac_jwt_secret_key: str = "CHANGE_ME_TO_A_RANDOM_SECRET"
    """用于验证来自 RBAC 服务签发的 JWT 的密钥。"""

    rbac_jwt_algorithm: str = "HS256"
    """JWT 加密算法，需与 RBAC 服务保持一致。"""

    log_audit_base_url: AnyHttpUrl | None = None
    """日志 / 审计服务基础地址，未配置则网关不上报审计日志。"""

    log_detective_base_url: str = "http://localhost:9003"
    """日志侦探服务基础地址"""

    class Config:
        env_prefix = "GATEWAY_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取全局配置实例，使用 lru_cache 缓存避免重复解析环境变量。"""
    return Settings()


settings = get_settings()
