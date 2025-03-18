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


def provide_rabbitmq_factories(provider: Provider) -> None:
    """Создание фабрик для RabbitMQ."""
    provider.provide(amqp_conn_pool, scope=Scope.APP, provides=Pool[AbstractConnection])
    provider.provide(amqp_channel_pool, scope=Scope.APP, provides=Pool[AbstractChannel])
    provider.provide(setup_channel, scope=Scope.REQUEST, provides=AbstractChannel)
    provider.provide(MessagePublisherImpl, scope=Scope.REQUEST, provides=MessagePublisher)
    provider.provide(EventBusImpl, scope=Scope.REQUEST, provides=EventBus)
