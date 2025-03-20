from dishka import Provider, Scope, from_context

from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.db.postgres.config import PostgresConfig


class ConfigsProvider(Provider):
    """Провайдер конфигураций."""

    scope = Scope.APP

    rabbit_config = from_context(RabbitMQConfig)
    postgres_config = from_context(PostgresConfig)
