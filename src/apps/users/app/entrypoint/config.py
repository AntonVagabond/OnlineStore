import os
from dataclasses import dataclass
from typing import Self

from dotenv import load_dotenv

from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.db.postgres.config import PostgresConfig

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Класс конфигурации приложения."""

    openapi_url: str
    client_id: str
    client_secret: str
    page_size: int

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки приложения."""
        openapi_url = os.getenv("OPENAPI_URL", "/swagger/docs/v1.0/users")
        client_id = os.getenv("CLIENT_ID", "fastapi")
        client_secret = os.getenv("CLIENT_SECRET", "fastapi_secret")
        page_size = int(os.getenv("PAGE_SIZE", 10))

        return cls(
            openapi_url=openapi_url,
            client_id=client_id,
            client_secret=client_secret,
            page_size=page_size,
        )


@dataclass(frozen=True)
class Config:
    postgres_config: PostgresConfig
    rabbitmq_config: RabbitMQConfig
    app_config: AppConfig


def create_config() -> Config:
    return Config(
        postgres_config=PostgresConfig.from_env(),
        rabbitmq_config=RabbitMQConfig.from_env(),
        app_config=AppConfig.from_env(),
    )
