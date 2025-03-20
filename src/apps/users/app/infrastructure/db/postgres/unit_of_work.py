from app.application.common.unit_of_work import UnitOfWork
from app.domain.common.entity import Entity
from app.infrastructure.db.postgres.interfaces.transaction import Transaction

from .interfaces.registry import Registry


class UnitOfWorkImpl(UnitOfWork):
    """Класс реализующий UnitOfWork."""

    def __init__(self, registry: Registry, transaction: Transaction) -> None:
        self.__registry = registry
        self.__transaction = transaction

        self.__new_entities: list[Entity] = []
        self.__dirty_entities: list[Entity] = []
        self.__deleted_entities: list[Entity] = []

    def register_new(self, entity: Entity) -> None:
        """Реализация регистрации новой сущности."""
        self.__new_entities.append(entity)

    def register_dirty(self, entity: Entity) -> None:
        """Реализация регистрации изменения существующей сущности."""
        self.__dirty_entities.append(entity)

    def register_deleted(self, entity: Entity) -> None:
        """Реализация регистрации удаления существующей сущности."""
        self.__deleted_entities.append(entity)

    async def __add_entities(self) -> None:
        """Добавить сущности."""
        for entity in self.__new_entities:
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.add(entity=entity)

    async def __update_entities(self) -> None:
        """Обновить сущности."""
        for entity in self.__dirty_entities:
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.update(entity)

    async def __delete_entities(self) -> None:
        """Удалить сущности."""
        for entity in self.__deleted_entities:
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.delete(entity)

    async def commit(self) -> None:
        """Реализация фиксирования транзакции."""
        try:
            await self.__add_entities()
            await self.__update_entities()
            await self.__delete_entities()

            await self.__transaction.commit()
        except Exception as exc:
            await self.__transaction.rollback()
            raise exc
