from dishka import Provider, Scope

from app.infrastructure.brokers.rabbit.config import RabbitMQConfig
from app.infrastructure.db.postgres.config import PostgresConfig


def provide_configs(provider: Provider):
    """Провайдер конфигураций."""
    provider.from_context(RabbitMQConfig, scope=Scope.APP)
    provider.from_context(PostgresConfig, scope=Scope.APP)
