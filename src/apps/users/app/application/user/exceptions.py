from ..common.exception import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    """Такой пользователь уже существует."""


class EmailAlreadyExistsError(ApplicationError):
    """Этот email уже используется."""


class PhoneNumberAlreadyExistsError(ApplicationError):
    """Этот номер телефона уже используется."""


class UserNotFoundError(ApplicationError):
    """Пользователь не найден."""
