from app.domain.common.exception import DomainError


class ProfileNotFoundError(DomainError):
    """Профиль пользователя не найден."""
