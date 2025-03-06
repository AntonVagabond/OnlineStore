from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.common.unit_of_work import IUnitOfWork
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import IUserRepository
from app.infrastructure.db.postgres.config import PostgresConfig
from app.infrastructure.db.postgres.engine import setup_engine, setup_session
from app.infrastructure.db.postgres.gateways.mappers.user_mapper import UserDataMapper
from app.infrastructure.db.postgres.gateways.repositories.user_repository import (
    UserRepository,
)
from app.infrastructure.db.postgres.interfaces.registry import IRegistry
from app.infrastructure.db.postgres.registry import Registry
from app.infrastructure.db.postgres.unit_of_work import UnitOfWork


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
    def provide_user_repository(self, session: AsyncSession) -> IUserRepository:
        """Получение репозитория пользователями для работы с CUD-операциями."""
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_user_data_mapper(self, session: AsyncSession) -> UserDataMapper:
        """Получение преобразователя данных для сущности User."""
        return UserDataMapper(session)

    @provide(scope=Scope.REQUEST)
    def provide_registry(self, user_data_mapper: UserDataMapper) -> IRegistry:
        """Регистрируем у каждой сущности свой преобразователь данных."""
        registry = Registry()
        registry.register_mapper(User, user_data_mapper)
        return registry

    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(
        self, session: AsyncSession, registry: IRegistry
    ) -> IUnitOfWork:
        """Получение UnitOfWork для работы с транзакциями."""
        return UnitOfWork(registry, session)
