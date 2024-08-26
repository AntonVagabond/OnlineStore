from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import get_settings, settings

engine_async = create_async_engine(str(settings.db.async_database_uri))
async_session_maker = async_sessionmaker(engine_async)
