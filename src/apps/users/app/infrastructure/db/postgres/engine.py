from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.infrastructure.db.postgres.config import PostgresConfig


async def setup_engine(config: PostgresConfig) -> AsyncGenerator[AsyncEngine, None]:
    """Создание асинхронного движка для PostgreSQL."""
    engine = create_async_engine(config.postgres_dsn, echo=config.echo)
    yield engine
    await engine.dispose()


async def setup_connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    """Создание асинхронного подключения к PostgreSQL."""
    async with engine.begin() as connection:
        yield connection
