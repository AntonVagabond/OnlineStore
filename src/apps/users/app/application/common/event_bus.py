from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.domain.common.event import Event


class EventBus(Protocol):
    """Протокол для ведения журнала событий."""

    @abstractmethod
    async def publish(self, events: list[Event]) -> None:
        """Отправить события в очередь."""
        raise NotImplementedError("Метод должен быть реализован подклассами.")
