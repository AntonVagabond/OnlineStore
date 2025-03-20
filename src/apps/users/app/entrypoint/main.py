from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aio_pika.abc import AbstractChannel
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.brokers.rabbit.setup import (
    bind_queue_to_exchange,
    declare_exchange,
    declare_queues,
)
from app.infrastructure.common.config import create_config
from app.presentation.api.setups.exception import setup_exception_handlers
from app.presentation.api.setups.routers import setup_routers

from .di.setup import setup_container
from .setup import setup_app


async def declare_amqp_bindings(async_container: AsyncContainer) -> None:
    """Привязка между обменником и очередью AMQP."""
    async with async_container() as request_container:
        channel = await request_container.get(AbstractChannel)
        exchange = await declare_exchange(channel)
        queue = await declare_queues(channel)
        await bind_queue_to_exchange(queue, exchange)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa
    await declare_amqp_bindings(async_container=app.state.dishka_container)
    yield


def app_factory() -> FastAPI:
    """Точка старта приложения."""

    config = create_config()
    container = setup_container(config=config)
    app = setup_app(lifespan=lifespan, config=config.app_config)
    setup_routers(app)
    setup_exception_handlers(app)
    setup_dishka(container=container, app=app)
    return app
