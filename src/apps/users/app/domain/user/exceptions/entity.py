from ...common.exception import DomainError


class UserAlreadyExistsError(DomainError):
    """Такой пользователь уже существует."""


class EmailAlreadyExistsError(DomainError):
    """Этот email уже используется."""


class PhoneNumberAlreadyExistsError(DomainError):
    """Этот номер телефона уже используется."""


class UserNotFoundError(DomainError):
    """Пользователь не найден."""
