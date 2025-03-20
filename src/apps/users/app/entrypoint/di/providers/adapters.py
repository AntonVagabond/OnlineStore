from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.persistence.user_reader import UserReader
from app.application.common.unit_of_work import UnitOfWork
from app.domain.common.id_generator import IdGenerator
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import UserRepository
from app.infrastructure.adapters.id_generator import IdGeneratorImpl
from app.infrastructure.db.postgres.gateways.mappers.user_mapper import UserDataMapper
from app.infrastructure.db.postgres.gateways.readers.user_reader import UserReaderImpl
from app.infrastructure.db.postgres.gateways.repositories.user_repository import (
    UserRepositoryImpl,
)
from app.infrastructure.db.postgres.interfaces.registry import Registry
from app.infrastructure.db.postgres.interfaces.transaction import Transaction
from app.infrastructure.db.postgres.registry import RegistryImpl
from app.infrastructure.db.postgres.unit_of_work import UnitOfWorkImpl


class AdaptersProvider(Provider):
    """Провайдер для адаптеров."""

    scope = Scope.REQUEST

    user_repository = provide(UserRepositoryImpl, provides=UserRepository)
    user_reader = provide(UserReaderImpl, provides=UserReader)
    id_generator = provide(IdGeneratorImpl, provides=IdGenerator)
    transaction = alias(AsyncSession, provides=Transaction)

    user_data_mapper = provide(UserDataMapper)

    @provide
    def provide_registry(self, user_data_mapper: UserDataMapper) -> Registry:
        registry = RegistryImpl()
        registry.register_mapper(User, user_data_mapper)
        return registry

    unit_of_work = provide(UnitOfWorkImpl, provides=UnitOfWork)
