from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.unit_of_work import IUnitOfWork
from app.domain.common.entity import Entity

if TYPE_CHECKING:
    from app.infrastructure.db.postgres.interfaces.registry import IRegistry


class UnitOfWork(IUnitOfWork):
    """Класс реализующий UnitOfWork."""

    def __init__(self, registry: IRegistry, session: AsyncSession) -> None:
        self.__new: dict[UUID, Entity] = {}
        self.__dirty: dict[UUID, Entity] = {}
        self.__deleted: dict[UUID, Entity] = {}
        self.__registry = registry
        self.__session = session

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
        for entity in self.__new.values():
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.add(entity)

        for entity in self.__dirty.values():
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.update(entity)

        for entity in self.__deleted.values():
            mapper = self.__registry.get_mapper(entity=type(entity))
            await mapper.delete(entity)

    async def commit(self) -> None:
        """Реализация фиксирования транзакции."""
        await self.__flush()
        await self.__session.commit()
