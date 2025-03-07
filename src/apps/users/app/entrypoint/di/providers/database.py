from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.common.persistence.user_reader import UserReader
from app.application.common.unit_of_work import UnitOfWork
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import UserRepository
from app.infrastructure.db.postgres.config import PostgresConfig
from app.infrastructure.db.postgres.engine import setup_engine, setup_session
from app.infrastructure.db.postgres.gateways.mappers.user_mapper import UserDataMapper
from app.infrastructure.db.postgres.gateways.readers.user_reader import UserReaderImpl
from app.infrastructure.db.postgres.gateways.repositories.user_repository import (
    UserRepositoryImpl,
)
from app.infrastructure.db.postgres.interfaces.registry import Registry
from app.infrastructure.db.postgres.registry import RegistryImpl
from app.infrastructure.db.postgres.unit_of_work import UnitOfWorkImpl


class PostgresDatabaseProvider(Provider):
    """Провайдер для PostgreSQL."""

    @provide(scope=Scope.APP)
    def provide_postgres_config(self) -> PostgresConfig:
        """Получение конфигурации для подключения к PostgreSQL."""
        return PostgresConfig()

    @provide(scope=Scope.APP, provides=AsyncEngine)
    async def provide_postgres_engine(
        self, config: PostgresConfig
    ) -> AsyncGenerator[AsyncEngine, None]:
        """Создание асинхронного движка для PostgreSQL."""
        return setup_engine(config)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_postgres_connection(
        self, engine: AsyncEngine
    ) -> AsyncGenerator[AsyncSession, None]:
        """Создание асинхронного соединения с PostgreSQL."""
        return setup_session(engine)

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(
        self, uow: UnitOfWork, session: AsyncSession
    ) -> UserRepository:
        """Внедрение зависимости для репозитория пользователей."""
        return UserRepositoryImpl(uow, session)

    @provide(scope=Scope.REQUEST)
    def provide_user_reader(self, session: AsyncSession) -> UserReader:
        """Внедрение зависимости для чтения пользователей."""
        return UserReaderImpl(session)

    @provide(scope=Scope.REQUEST)
    def provide_user_data_mapper(self, session: AsyncSession) -> UserDataMapper:
        """Внедрение зависимости преобразователя данных для сущности User."""
        return UserDataMapper(session)

    @provide(scope=Scope.REQUEST)
    def provide_registry(self, user_data_mapper: UserDataMapper) -> Registry:
        """Регистрируем у каждой сущности свой преобразователь данных."""
        registry = RegistryImpl()
        registry.register_mapper(User, user_data_mapper)
        return registry

    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(
        self, session: AsyncSession, registry: Registry
    ) -> UnitOfWork:
        """Внедрение зависимости UnitOfWork для работы с транзакциями."""
        return UnitOfWorkImpl(registry, session)
