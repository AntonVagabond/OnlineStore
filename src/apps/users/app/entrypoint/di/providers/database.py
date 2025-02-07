from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.infrastructure.db.postgres.config import PostgresConfig
from app.infrastructure.db.postgres.engine import setup_connection, setup_engine


class PostgresDatabaseProvider(Provider):
    """Провайдер для работы с PostgreSQL."""

    @provide(scope=Scope.APP)
    def provide_postgres_config(self) -> PostgresConfig:
        """Получение конфигурации для подключения к PostgreSQL."""
        return PostgresConfig()

    @provide(scope=Scope.APP, provides=AsyncEngine)
    def provide_postgres_engine(
        self, config: PostgresConfig
    ) -> AsyncGenerator[AsyncEngine, None]:
        """Создание асинхронного движка для PostgreSQL."""
        return setup_engine(config)

    @provide(scope=Scope.REQUEST, provides=AsyncConnection)
    def provide_postgres_connection(
        self, engine: AsyncEngine
    ) -> AsyncGenerator[AsyncConnection, None]:
        """Создание асинхронного соединения с PostgreSQL."""
        return setup_connection(engine)
