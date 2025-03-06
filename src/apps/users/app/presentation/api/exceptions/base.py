from dataclasses import dataclass


@dataclass(eq=False)
class PresentationError(Exception):
    """Общий класс представительского уровня ошибок."""

    message: str
