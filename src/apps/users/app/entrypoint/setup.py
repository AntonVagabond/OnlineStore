import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from aio_pika.abc import AbstractChannel
from dishka import AsyncContainer
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.entrypoint.config import AppConfig
from app.entrypoint.di.setup import container
from app.infrastructure.brokers.rabbit.setup import (
    bind_queue_to_exchange,
    declare_exchange,
    declare_queues,
)


async def get_app_config(async_container: AsyncContainer) -> AppConfig:
    """Получить настройки приложения."""
    async with async_container() as request_container:
        return await request_container.get(AppConfig)


async def declare_amqp_bindings(async_container: AsyncContainer) -> None:
    """Привязка между обменником и очередью AMQP."""
    async with async_container() as request_container:
        channel = await request_container.get(AbstractChannel)
        exchange = await declare_exchange(channel)
        queue = await declare_queues(channel)
        await bind_queue_to_exchange(queue, exchange)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa
    await declare_amqp_bindings(async_container=container)
    yield


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """Swagger configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User",
        version="1.0",
        summary="Микросервис для работы с профилем пользователя.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_app() -> FastAPI:
    """Настройка приложения."""
    settings = asyncio.run(get_app_config(async_container=container))
    app = FastAPI(
        lifespan=lifespan,
        openapi_url=settings.openapi_url,
        swagger_ui_init_oauth={
            "clientId": settings.client_id,
            "clientSecret": settings.client_secret,
        },
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )
    app.openapi = lambda: custom_openapi(app)
    return app
