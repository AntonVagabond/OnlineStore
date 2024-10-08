from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings

engine_async = create_async_engine(settings.db.async_database_url)
async_session_maker = async_sessionmaker(engine_async)
