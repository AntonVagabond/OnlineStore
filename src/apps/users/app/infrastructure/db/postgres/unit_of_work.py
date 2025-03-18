from uuid import UUID

from dishka import AsyncContainer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.unit_of_work import UnitOfWork
from app.domain.common.entity import Entity
from app.infrastructure.db.postgres.interfaces.registry import Registry


class UnitOfWorkImpl(UnitOfWork):
    """Класс реализующий UnitOfWork."""

    def __init__(
        self, registry: Registry, session: AsyncSession, container: AsyncContainer
    ) -> None:
        self.__new: dict[UUID, Entity] = {}
        self.__dirty: dict[UUID, Entity] = {}
        self.__deleted: dict[UUID, Entity] = {}
        self.__registry = registry
        self.__session = session
        self.__container = container

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
            mapper_type = self.__registry.get_mapper_type(entity=type(entity))
            mapper = await self.__container.get(mapper_type)
            await mapper.add(entity=entity)

        for entity in self.__dirty.values():
            mapper_type = self.__registry.get_mapper_type(entity=type(entity))
            mapper = await self.__container.get(mapper_type)
            await mapper.update(entity)

        for entity in self.__deleted.values():
            mapper_type = self.__registry.get_mapper_type(entity=type(entity))
            mapper = await self.__container.get(mapper_type)
            await mapper.delete(entity)

    async def commit(self) -> None:
        """Реализация фиксирования транзакции."""
        await self.__flush()
        await self.__session.commit()
