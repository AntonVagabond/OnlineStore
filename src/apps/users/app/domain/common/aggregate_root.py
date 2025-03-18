from abc import ABC
from typing import TypeVar

from .entity import Entity
from .event import Event

TEntityID = TypeVar("TEntityID")


class AggregateRoot(Entity[TEntityID], ABC):
    """Класс для взаимодействия сущностей с объектами значений и записи их событий."""

    __slots__ = ("entity_id", "__events")

    def __init__(self, entity_id: TEntityID):
        super().__init__(entity_id=entity_id)
        self.__events: list[Event] = []

    def record_event(self, event: Event) -> None:
        """Записать событие в историю событий."""
        self.__events.append(event)

    def raise_events(self) -> list[Event]:
        """Получить и очистить события."""
        events = self.__events.copy()
        self.__events.clear()

        return events
