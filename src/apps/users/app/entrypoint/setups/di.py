from dishka import AsyncContainer, Provider, make_async_container

from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.db.postgres.config import PostgresConfig

from ..config import Config
from ..di import providers


def setup_provider() -> Provider:
    """Создание провайдера."""

    provider = Provider()

    providers.provide_configs(provider)
    providers.provide_db_gateways(provider)
    providers.provide_db_connections(provider)
    providers.provide_db_unit_of_work(provider)

    return provider


def setup_container(provider: Provider, config: Config) -> AsyncContainer:
    """Создание DI-контейнера."""
    return make_async_container(
        provider,
        context={
            RabbitMQConfig: config.rabbitmq_config,
            PostgresConfig: config.postgres_config,
        },
    )
