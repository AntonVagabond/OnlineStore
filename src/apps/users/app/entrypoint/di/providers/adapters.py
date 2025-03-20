from dishka import Provider, Scope, WithParents, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities.user import User
from app.infrastructure.common.adapters.id_generator import IdGeneratorImpl
from app.infrastructure.db.postgres.persistence.adapters import (
    RegistryImpl,
    UnitOfWorkImpl,
    mappers,
    readers,
    repositories,
)
from app.infrastructure.db.postgres.persistence.registry import Registry
from app.infrastructure.db.postgres.persistence.transaction import Transaction


class AdaptersProvider(Provider):
    """Провайдер для адаптеров."""

    scope = Scope.REQUEST

    transaction = alias(AsyncSession, provides=Transaction)
    id_generator = provide(WithParents[IdGeneratorImpl])

    user_repository = provide(WithParents[repositories.UserRepositoryImpl])
    user_reader = provide(WithParents[readers.UserReaderImpl])
    user_data_mapper = provide(mappers.UserDataMapper)

    @provide
    def provide_registry(self, user_data_mapper: mappers.UserDataMapper) -> Registry:
        registry = RegistryImpl()
        registry.register_mapper(User, user_data_mapper)
        return registry

    unit_of_work = provide(WithParents[UnitOfWorkImpl])
