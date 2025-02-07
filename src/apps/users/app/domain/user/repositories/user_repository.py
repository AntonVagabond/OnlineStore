from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

if TYPE_CHECKING:
    from ..entities.user import User


class IUserRepository(Protocol):
    """Протокол для репозитория пользователей."""

    @abstractmethod
    async def load(self, user_id: UUID) -> User | None:
        """Получить пользователя по идентификатору."""
        raise NotImplementedError

    @abstractmethod
    async def is_exists_phone_number(self, phone_number: str) -> User | None:
        """Проверка на существование номера телефона."""
        raise NotImplementedError

    @abstractmethod
    async def is_exists_email(self, email: str) -> User | None:
        """Проверка на существование почты."""
        raise NotImplementedError

    @abstractmethod
    async def is_exists_username(self, username: str) -> User | None:
        """Проверка на существование никнейма у пользователя."""
        raise NotImplementedError
