from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ValueObject(Protocol):
    """Протокол для объектов значений."""

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Проверка валидности значения."""
        raise NotImplementedError
