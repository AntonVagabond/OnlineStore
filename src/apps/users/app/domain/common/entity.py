from abc import ABC
from typing import Generic, TypeVar

TEntityID = TypeVar("TEntityID")


class Entity(ABC, Generic[TEntityID]):
    """Базовый класс сущности."""

    def __init__(self, entity_id: TEntityID) -> None:
        self.entity_id = entity_id

    def __eq__(self, other: object) -> bool:
        """Метод для сравнения сущностей."""
        if isinstance(other, Entity):
            return bool(self.entity_id == other.entity_id)
        return False

    def __hash__(self) -> int:
        """Метод для получения хэша сущности."""
        return hash(self.entity_id)
