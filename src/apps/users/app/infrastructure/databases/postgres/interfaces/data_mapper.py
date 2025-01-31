from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domain.common.entity import Entity


class DataMapper(Protocol):
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
