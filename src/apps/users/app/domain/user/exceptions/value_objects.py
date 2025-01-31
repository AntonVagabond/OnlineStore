from dataclasses import dataclass

from app.domain.common.exception import DomainError


@dataclass(eq=False)
class InvalidUsernameError(DomainError):
    """Некорректное имя пользователя."""


@dataclass(eq=False)
class InvalidContactsError(DomainError):
    """Некорректные контактные данные."""
