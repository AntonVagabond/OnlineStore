from dataclasses import dataclass

from ...common.exception import DomainError


@dataclass(eq=False)
class InvalidUsernameError(DomainError):
    """Некорректное имя пользователя."""


@dataclass(eq=False)
class InvalidContactsError(DomainError):
    """Некорректные контактные данные."""
