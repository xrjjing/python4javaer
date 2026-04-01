"""
日志 / 审计服务配置模块。

职责：
- 提供数据库连接地址等运行参数；
- 作为 database.py / main.py 的共同配置入口。

排查建议：
- 服务启动后连不上库，先看这里的 database_url。
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
# 模块级单例：database.py / main.py 直接复用这份配置。
