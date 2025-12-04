# app/config.py
"""
配置管理：依赖链的起点
Java 对比：Spring @ConfigurationProperties
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，生产环境通过环境变量覆盖"""
    # 默认使用 SQLite 文件数据库；生产可改为 PostgreSQL/MySQL
    database_url: str = "sqlite:///./lab02.db"
    # 是否打印 SQL（调试用）
    echo_sql: bool = False

    class Config:
        env_prefix = "LAB02_"  # 环境变量前缀：LAB02_DATABASE_URL


@lru_cache
def get_settings() -> Settings:
    """
    依赖链起点：获取配置
    使用 lru_cache 确保单例，避免每请求重复加载
    """
    return Settings()
