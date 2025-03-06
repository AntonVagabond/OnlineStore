from dataclasses import dataclass

from ...common.exception import DomainError


@dataclass(eq=False)
class EmptyUsernameError(DomainError):
    """Имя пользователя не может быть пустым."""


@dataclass(eq=False)
class TooLongUsernameError(DomainError):
    """Имя пользователя слишком длинное."""


@dataclass(eq=False)
class WrongUsernameFormatError(DomainError):
    """Неверный формат имени пользователя."""


@dataclass(eq=False)
class InvalidContactsError(DomainError):
    """Некорректные контактные данные."""


@dataclass(eq=False)
class EmptyContactError(DomainError):
    """Контактный номер или почта не указаны."""


@dataclass(eq=False)
class WrongPhoneNumberFormatError(DomainError):
    """Неверный формат номера телефона."""


@dataclass(eq=False)
class WrongEmailFormatError(DomainError):
    """Неверный формат почты."""
