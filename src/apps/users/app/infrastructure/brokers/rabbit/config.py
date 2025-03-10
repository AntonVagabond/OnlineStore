import enum
import os
from dataclasses import dataclass
from typing import Self

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class RabbitMQConfig:
    """Класс конфигурации для RabbitMQ."""

    host: str
    port: int
    user: str
    password: str

    dsn: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки RabbitMQ."""
        host = os.getenv("RABBITMQ_HOST", "localhost")
        port = int(os.getenv("RABBITMQ_PORT", 5672))
        user = os.getenv("RABBITMQ_USER", "guest")
        password = os.getenv("RABBITMQ_PASSWORD", "guest")

        dsn = f"amqp://{user}:{password}@{host}:{port}"

        return cls(host=host, port=port, user=user, password=password, dsn=dsn)


class Exchanges(enum.StrEnum):
    """Класс перечисления обменников."""

    USER_EXCHANGE = "user_exchange"


class Queues(enum.StrEnum):
    """Класс перечисления очередей."""

    USER_QUEUE = "user_queue"
