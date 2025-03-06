from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.entrypoint.di.providers.app import AppConfigProvider
from app.entrypoint.di.providers.broker import RabbitMQProvider
from app.entrypoint.di.providers.database import PostgresDatabaseProvider
from app.entrypoint.di.providers.handlers import HandlersProvider


def setup_container() -> AsyncContainer:
    """Создание контейнера DI."""
    return make_async_container(
        AppConfigProvider(),
        PostgresDatabaseProvider(),
        HandlersProvider(),
        RabbitMQProvider(),
    )


def setup_di(app: FastAPI) -> None:
    """Инициализация контейнера DI."""
    setup_dishka(setup_container(), app)


container = setup_container()
