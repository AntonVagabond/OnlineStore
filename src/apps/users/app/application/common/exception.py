from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):
    """Общей класс для ошибок приложения."""

    message: str
