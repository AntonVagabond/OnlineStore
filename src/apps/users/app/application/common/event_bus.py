from abc import abstractmethod
from typing import Protocol

from app.domain.common.event import Event


class EventBus(Protocol):
    """Протокол для ведения журнала событий."""

    @abstractmethod
    async def publish(self, events: list[Event]) -> None:
        """Отправить события в очередь."""
        raise NotImplementedError
