from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    """Общей класс для доменных ошибок."""

    message: str
