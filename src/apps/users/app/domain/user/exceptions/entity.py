from app.domain.common.exception import DomainError


class UserAlreadyExistsError(DomainError):
    """Такой пользователь уже существует."""


class UserNotFoundError(DomainError):
    """Пользователь не найден."""
