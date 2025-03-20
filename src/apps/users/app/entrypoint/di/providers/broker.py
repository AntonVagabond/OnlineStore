from typing import AsyncGenerator

from aio_pika.abc import AbstractChannel, AbstractConnection
from aio_pika.pool import Pool
from dishka import Provider, Scope, provide

from app.application.common.event_bus import EventBus
from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.brokers.rabbit.interfaces.publisher import MessagePublisher
from app.infrastructure.brokers.rabbit.publisher import MessagePublisherImpl
from app.infrastructure.brokers.rabbit.setup import (
    amqp_channel_pool,
    amqp_conn_pool,
    setup_channel,
)
from app.infrastructure.events.event_bus import EventBusImpl


class RabbitMQProvider(Provider):
    """Провайдер для RabbitMQ."""

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_conn_pool(
        self, config: RabbitMQConfig
    ) -> AsyncGenerator[Pool[AbstractConnection], None]:
        """Подключение к пулу соединений для создания каналов."""
        async for conn_pool in amqp_conn_pool(config):
            yield conn_pool

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_channel_pool(
        self, connection_pool: Pool[AbstractConnection]
    ) -> AsyncGenerator[Pool[AbstractChannel], None]:
        """Подключение к пулу каналов."""
        async for channel_pool in amqp_channel_pool(connection_pool):
            yield channel_pool

    @provide(scope=Scope.REQUEST)
    async def provide_setup_channel(
        self, channel_pool: Pool[AbstractChannel]
    ) -> AsyncGenerator[AbstractChannel, None]:
        """Подключение к конкретному каналу из пула каналов."""
        async for channel in setup_channel(channel_pool):
            yield channel

    @provide(scope=Scope.REQUEST)
    async def provide_message_publisher(
        self, channel: AbstractChannel
    ) -> MessagePublisher:
        """Подключение к издателю сообщений."""
        return MessagePublisherImpl(channel)

    @provide(scope=Scope.REQUEST)
    async def provide_event_bus(self, message_publisher: MessagePublisher) -> EventBus:
        """Подключение к шине событий."""
        return EventBusImpl(message_publisher)
