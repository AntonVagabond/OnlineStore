from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.infrastructure.db.postgres.config import PostgresConfig
from app.infrastructure.db.postgres.engine import (
    setup_engine,
    setup_session,
    setup_session_maker,
)


class PostgresDatabaseProvider(Provider):
    """Провайдер для PostgreSQL."""

    @provide(scope=Scope.APP)
    def provide_postgres_engine(self, config: PostgresConfig) -> AsyncEngine:
        """Создание асинхронного движка для PostgreSQL."""
        return setup_engine(config)

    @provide(scope=Scope.APP)
    def provide_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        """Создание асинхронного сеанса с PostgreSQL."""
        return setup_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        """Создание асинхронной сессии."""
        async for session in setup_session(session_maker):
            yield session
