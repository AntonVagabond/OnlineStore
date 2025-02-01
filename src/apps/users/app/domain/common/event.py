from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4

EV = TypeVar("EV", bound=str)


@dataclass(frozen=True)
class Event(Generic[EV]):
    """Базовый класс События."""

    event_uuid: UUID = field(default_factory=uuid4, init=False, kw_only=True)
    event_date: datetime = field(
        default_factory=lambda: datetime.now(UTC), init=False, kw_only=True
    )
    event_type: str = field(default=EV, kw_only=True)

    def __str__(self) -> str:
        """Возвращает строковое представление события."""
        return f"{self.__class__.__name__}({self.event_uuid})"

    def __repr__(self) -> str:
        """Возвращает форматированное представление события."""
        return str(self)
