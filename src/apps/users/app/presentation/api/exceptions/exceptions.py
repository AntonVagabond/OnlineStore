from dataclasses import dataclass

from app.presentation.api.exceptions.base import PresentationError


@dataclass(eq=False)
class UnauthorizedError(PresentationError):
    """Ответ при не авторизованном пользователе."""
