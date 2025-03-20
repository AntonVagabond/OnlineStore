from abc import ABC, abstractmethod

from app.domain.common.entity import Entity


class DataMapper(ABC):
    """Протокол преобразователя данных."""

    @abstractmethod
    async def add(self, entity: Entity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: Entity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Entity) -> None:
        raise NotImplementedError
