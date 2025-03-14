from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    """Базовый класс События."""

    event_uuid: UUID = field(default_factory=uuid4, init=False, kw_only=True)
    event_date: datetime = field(
        default_factory=lambda: datetime.now(UTC), init=False, kw_only=True
    )
    event_type: str = field(kw_only=True)

    def __str__(self) -> str:
        """Возвращает строковое представление события."""
        return f"{self.__class__.__name__}({self.event_uuid})"

    def __repr__(self) -> str:
        """Возвращает форматированное представление события."""
        return str(self)
