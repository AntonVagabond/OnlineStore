from dishka import AsyncContainer, Provider, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.application.common.persistence.user_reader import UserReader
from app.application.common.unit_of_work import UnitOfWork
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import UserRepository
from app.infrastructure.db.postgres.engine import (
    setup_engine,
    setup_session,
    setup_session_maker,
)
from app.infrastructure.db.postgres.gateways.mappers.user_mapper import UserDataMapper
from app.infrastructure.db.postgres.gateways.readers.user_reader import UserReaderImpl
from app.infrastructure.db.postgres.gateways.repositories.user_repository import (
    UserRepositoryImpl,
)
from app.infrastructure.db.postgres.interfaces.registry import Registry
from app.infrastructure.db.postgres.registry import RegistryImpl
from app.infrastructure.db.postgres.unit_of_work import UnitOfWorkImpl


def setup_data_mappers() -> Registry:
    """Создание регистра для преобразователей данных."""
    registry = RegistryImpl()

    registry.register_mapper(User, UserDataMapper)  # type: ignore

    return registry


def provide_resolver(provider: Provider) -> None:
    """Внедрение распознавателя зависимости."""
    provider.provide(AsyncContainer, scope=Scope.REQUEST)


def provide_db_gateways(provider: Provider) -> None:
    """Внедрение зависимостей для работы с БД."""
    provider.provide(UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository)
    provider.provide(UserReaderImpl, scope=Scope.REQUEST, provides=UserReader)
    provider.provide(UserDataMapper, scope=Scope.REQUEST, provides=UserDataMapper)


def provide_db_connections(provider: Provider) -> None:
    """Создание асинхронного движка и создание сессии PostgreSQL."""
    provider.provide(setup_engine, scope=Scope.APP, provides=AsyncEngine)
    provider.provide(
        setup_session_maker, scope=Scope.APP, provides=async_sessionmaker[AsyncSession]
    )
    provider.provide(setup_session, scope=Scope.REQUEST, provides=AsyncSession)


def provide_db_unit_of_work(provider: Provider) -> None:
    """Внедрение зависимости UnitOfWork для работы с транзакциями."""
    provider.provide(setup_data_mappers, scope=Scope.REQUEST, provides=Registry)
    provider.provide(UnitOfWorkImpl, scope=Scope.REQUEST, provides=UnitOfWork)
