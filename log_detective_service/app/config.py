"""配置管理"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "log_detective_service"
    SERVICE_PORT: int = 8084
    MAX_LOG_SIZE: int = 2_000_000  # 2MB
    MAX_LOG_LINES: int = 50_000
    REGEX_TIMEOUT: int = 2  # 秒
    MAX_REGEX_LENGTH: int = 500
    MAX_RESULTS: int = 1000

settings = Settings()
