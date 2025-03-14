from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.db.postgres.config import PostgresConfig


def setup_engine(config: PostgresConfig) -> AsyncEngine:
    """Создание асинхронного движка для PostgreSQL."""
    return create_async_engine(config.uri)


def setup_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Создание асинхронной фабрики сессий."""
    return async_sessionmaker(bind=engine)


async def setup_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Создание асинхронного подключения к PostgreSQL."""
    async with session_maker() as session:
        yield session
