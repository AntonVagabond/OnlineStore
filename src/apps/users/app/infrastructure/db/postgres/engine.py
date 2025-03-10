from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.db.postgres.config import PostgresConfig


async def setup_engine(config: PostgresConfig) -> AsyncGenerator[AsyncEngine, None]:
    """Создание асинхронного движка для PostgreSQL."""
    engine = create_async_engine(config.uri)
    yield engine
    await engine.dispose()


async def setup_session_maker(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Создание асинхронного подключения к PostgreSQL."""
    async with async_sessionmaker(engine) as session:
        yield session
