"""配置管理"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_mode: str = "mock"  # mock / real
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "admin"
    rabbitmq_pass: str = "admin123"
    queue_name: str = "learning_queue"

    class Config:
        env_file = ".env"


settings = Settings()
