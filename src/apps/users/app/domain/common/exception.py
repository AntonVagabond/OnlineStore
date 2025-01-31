from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    """Общее класс для доменных ошибок."""

    message: str
