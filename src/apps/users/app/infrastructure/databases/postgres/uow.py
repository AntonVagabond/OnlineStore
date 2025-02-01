from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain.common.entity import Entity

if TYPE_CHECKING:
    from app.infrastructure.common.protocols.unit_of_work import UnitOfWork
    from app.infrastructure.databases.postgres.interfaces.registry import Registry


class UnitOfWorkImpl(UnitOfWork):
    """Класс реализующий UnitOfWork."""

    def __init__(self, registry: Registry, connection: AsyncConnection) -> None:
        self.__new: dict[UUID, Entity] = {}
        self.__dirty: dict[UUID, Entity] = {}
        self.__deleted: dict[UUID, Entity] = {}
        self.__registry = registry
        self.__connection = connection

    def register_new(self, entity: Entity) -> None:
        """Реализация регистрации новой сущности."""
        self.__new[entity.entity_id] = entity

    def register_dirty(self, entity: Entity) -> None:
        """Реализация регистрации изменения существующей сущности."""
        if entity.entity_id not in self.__new:
            self.__dirty[entity.entity_id] = entity

    def register_deleted(self, entity: Entity) -> None:
        """Реализация регистрации удаления существующей сущности."""
        if entity.entity_id in self.__new:
            self.__new.pop(entity.entity_id)

        if entity.entity_id in self.__dirty:
            self.__dirty.pop(entity.entity_id)

        self.__deleted[entity.entity_id] = entity

    async def __flush(self) -> None:
        """Реализация фиксации изменений."""
        for entity_type, entity in self.new.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.add(entity)

        for entity_type, entity in self.dirty.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.update(entity)

        for entity_type, entity in self.deleted.items():
            mapper = self.registry.get_mapper(entity_type)
            await mapper.delete(entity)

    async def commit(self) -> None:
        """Реализация фиксирования транзакции."""
        await self.__flush()
        await self.__connection.commit()
