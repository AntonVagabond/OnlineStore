import enum
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AMQPConfig:
    """Класс конфигурации для RabbitMQ."""

    host: str = os.getenv("RABBITMQ_HOST", "localhost")
    port: int = int(os.getenv("RABBITMQ_PORT", 5672))
    user: str = os.getenv("RABBITMQ_USER", "guest")
    password: str = os.getenv("RABBITMQ_PASSWORD", "guest")

    @property
    def amqp_dsn(self) -> str:
        """Возвращает DSN для подключения к RabbitMQ."""
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class Exchanges(enum.StrEnum):
    """Класс перечисления обменников."""

    USER_EXCHANGE = "user_exchange"


class Queues(enum.StrEnum):
    """Класс перечисления очередей."""

    USER_QUEUE = "user_queue"
