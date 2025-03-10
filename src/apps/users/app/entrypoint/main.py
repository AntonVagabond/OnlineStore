from contextlib import asynccontextmanager

from aio_pika.abc import AbstractChannel
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.entrypoint.config import create_config
from app.entrypoint.setups.app import setup_app
from app.entrypoint.setups.di import setup_container, setup_provider
from app.infrastructure.brokers.rabbit.setup import (
    bind_queue_to_exchange,
    declare_exchange,
    declare_queues,
)
from app.presentation.api.setups.exception import setup_exception_handlers
from app.presentation.api.setups.routers import setup_routers


async def declare_amqp_bindings(async_container: AsyncContainer) -> None:
    """Привязка между обменником и очередью AMQP."""
    async with async_container() as request_container:
        channel = await request_container.get(AbstractChannel)
        exchange = await declare_exchange(channel)
        queue = await declare_queues(channel)
        await bind_queue_to_exchange(queue, exchange)


def app_factory() -> FastAPI:
    """Точка старта приложения."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa
        await declare_amqp_bindings(async_container=container)
        yield

    config = create_config()
    provider = setup_provider()
    container = setup_container(provider=provider, config=config)
    app = setup_app(lifespan=lifespan, config=config.app_config)
    setup_routers(app)
    setup_exception_handlers(app)
    setup_dishka(container=container, app=app)
    return app
