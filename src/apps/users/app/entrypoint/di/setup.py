from dishka import AsyncContainer, make_async_container

from app.entrypoint.di.providers.adapters import AdaptersProvider
from app.entrypoint.di.providers.broker import RabbitMQProvider
from app.entrypoint.di.providers.config import ConfigsProvider
from app.entrypoint.di.providers.database import PostgresDatabaseProvider
from app.entrypoint.di.providers.handlers import HandlersProvider
from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.common.config import Config
from app.infrastructure.db.postgres.config import PostgresConfig


def setup_container(config: Config) -> AsyncContainer:
    """Создание DI-контейнера."""
    return make_async_container(
        ConfigsProvider(),
        AdaptersProvider(),
        RabbitMQProvider(),
        PostgresDatabaseProvider(),
        HandlersProvider(),
        context={
            RabbitMQConfig: config.rabbitmq_config,
            PostgresConfig: config.postgres_config,
        },
    )
