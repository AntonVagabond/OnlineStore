from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domain.common.entity import Entity

    from .data_mapper import DataMapper


class IRegistry(Protocol):
    """Протокол регистрации преобразователей данных для сущностей."""

    @abstractmethod
    def register_mapper(self, entity: type[Entity], mapper: DataMapper) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_mapper(self, entity: type[Entity]) -> DataMapper:
        raise NotImplementedError
