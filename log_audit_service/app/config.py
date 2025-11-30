"""
日志 / 审计服务配置模块。

通过配置类统一管理配置，支持从环境变量或 .env 文件加载。
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """日志 / 审计服务配置类。"""

    database_url: str = "sqlite:///./log_audit.db"
    """数据库连接字符串，默认使用当前目录下的 SQLite 文件。"""

    class Config:
        env_prefix = "LOG_AUDIT_"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取全局配置实例，使用 lru_cache 缓存避免重复解析环境变量。"""
    return Settings()


settings = get_settings()
