from collections.abc import AsyncGenerator

from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractQueue,
    AbstractRobustConnection,
)
from aio_pika.pool import Pool

from .config import Exchanges, Queues, RabbitMQConfig

# ------------------------------ Not include in the DI -----------------------------------


async def amqp_connection(config: RabbitMQConfig) -> AbstractRobustConnection:
    """Подключение к rabbitmq."""
    return await connect_robust(url=config.dsn)


async def amqp_channel(connection_pool: Pool[AbstractConnection]) -> AbstractChannel:
    """Создание канала для обмена сообщениями."""
    async with connection_pool.acquire() as conn:
        return await conn.channel(publisher_confirms=False)


# ----------------------------------------------------------------------------------------


async def amqp_conn_pool(
    config: RabbitMQConfig,
) -> AsyncGenerator[Pool[AbstractConnection], None]:
    """Подключение к пулу соединений для создания каналов."""
    async with Pool(lambda: amqp_connection(config), max_size=15) as conn_pool:
        yield conn_pool


async def amqp_channel_pool(
    conn_pool: Pool[AbstractConnection],
) -> AsyncGenerator[Pool[AbstractChannel], None]:
    """Подключение к пулу каналов."""
    async with Pool(lambda: amqp_channel(conn_pool), max_size=105) as channel_pool:
        yield channel_pool


async def setup_channel(
    channel_pool: Pool[AbstractChannel],
) -> AsyncGenerator[AbstractChannel, None]:
    """Подключение к конкретному каналу из пула каналов."""
    async with channel_pool.acquire() as channel:
        yield channel


async def declare_exchange(channel: AbstractChannel) -> AbstractExchange:
    """Создание обменника."""
    return await channel.declare_exchange(
        name=Exchanges.USER_EXCHANGE, type=ExchangeType.TOPIC, durable=True
    )


async def declare_queues(channel: AbstractChannel) -> AbstractQueue:
    """Создание очереди."""
    return await channel.declare_queue(name=Queues.USER_QUEUE, durable=True)


async def bind_queue_to_exchange(
    queue: AbstractQueue, exchange: AbstractExchange
) -> None:
    """Привязка очереди к обменнику."""
    await queue.bind(exchange=exchange, routing_key="*")
