from aio_pika.abc import AbstractChannel, AbstractConnection
from aio_pika.pool import Pool
from dishka import Provider, Scope

from app.application.common.event_bus import EventBus
from app.infrastructure.brokers.rabbit.interfaces.publisher import MessagePublisher
from app.infrastructure.brokers.rabbit.publisher import MessagePublisherImpl
from app.infrastructure.brokers.rabbit.setup import (
    amqp_channel_pool,
    amqp_conn_pool,
    setup_channel,
)
from app.infrastructure.events.event_bus import EventBusImpl

# class RabbitMQProvider(Provider):
#     """Провайдер для RabbitMQ."""
#
#     @provide(scope=Scope.APP)
#     async def provide_rabbitmq_conn_pool(
#         self, config: Config
#     ) -> AsyncGenerator[Pool[AbstractConnection], None]:
#         """Подключение к пулу соединений для создания каналов."""
#         async for conn_pool in amqp_conn_pool(config.rabbitmq_config):
#             yield conn_pool
#
#     @provide(scope=Scope.APP)
#     async def provide_rabbitmq_channel_pool(
#         self, connection_pool: Pool[AbstractConnection]
#     ) -> AsyncGenerator[Pool[AbstractChannel], None]:
#         """Подключение к пулу каналов."""
#         async for channel_pool in amqp_channel_pool(connection_pool):
#             yield channel_pool
#
#     @provide(scope=Scope.REQUEST)
#     async def provide_setup_channel(
#         self, channel_pool: Pool[AbstractChannel]
#     ) -> AsyncGenerator[AbstractChannel, None]:
#         """Подключение к конкретному каналу из пула каналов."""
#         async for channel in setup_channel(channel_pool):
#             yield channel
#
#     @provide(scope=Scope.REQUEST)
#     async def provide_message_publisher(
#         self, channel: AbstractChannel
#     ) -> MessagePublisher:
#         """Подключение к издателю сообщений."""
#         return MessagePublisherImpl(channel)
#
#     @provide(scope=Scope.REQUEST)
#     async def provide_event_bus(self, message_publisher: MessagePublisher) -> EventBus:
#         """Подключение к шине событий."""
#         return EventBusImpl(message_publisher)


def provide_rabbitmq_factories(provider: Provider) -> None:
    """Создание фабрик для RabbitMQ."""
    provider.provide(amqp_conn_pool, scope=Scope.APP, provides=Pool[AbstractConnection])
    provider.provide(amqp_channel_pool, scope=Scope.APP, provides=Pool[AbstractChannel])
    provider.provide(setup_channel, scope=Scope.REQUEST, provides=AbstractChannel)
    provider.provide(MessagePublisherImpl, scope=Scope.REQUEST, provides=MessagePublisher)
    provider.provide(EventBusImpl, scope=Scope.REQUEST, provides=EventBus)
