from typing import AsyncGenerator

from aio_pika.abc import AbstractChannel, AbstractConnection
from aio_pika.pool import Pool
from dishka import Provider, Scope, provide

from app.infrastructure.brokers.rabbit.config import AMQPConfig
from app.infrastructure.brokers.rabbit.setup import (
    amqp_channel_pool,
    amqp_conn_pool,
    setup_channel,
)


class RabbitMQProvider(Provider):
    """Провайдер для RabbitMQ."""

    @provide(scope=Scope.APP)
    def provide_rabbitmq_config(self) -> AMQPConfig:
        """Получение конфигурации для подключения к RabbitMQ."""
        return AMQPConfig()

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_conn_pool(
        self, config: AMQPConfig
    ) -> AsyncGenerator[Pool[AbstractConnection], None]:
        """Подключение к пулу соединений для создания каналов."""
        return amqp_conn_pool(config)

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_channel_pool(
        self, connection_pool: Pool[AbstractConnection]
    ) -> AsyncGenerator[Pool[AbstractChannel], None]:
        """Подключение к пулу каналов."""
        return amqp_channel_pool(connection_pool)

    @provide(scope=Scope.REQUEST)
    async def provide_setup_channel(
        self, channel_pool: Pool[AbstractChannel]
    ) -> AsyncGenerator[AbstractChannel, None]:
        """Подключение к конкретному каналу из пула каналов."""
        return setup_channel(channel_pool)
