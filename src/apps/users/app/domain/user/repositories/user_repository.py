from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.user.entities.user import User


class UserRepository(Protocol):
    """Протокол для репозитория пользователей."""

    @abstractmethod
    async def load(self, user_id: UUID) -> User | None:
        """Загрузить пользователя по идентификатору."""
        raise NotImplementedError("Метод должен быть реализован подклассами.")

    @abstractmethod
    async def is_exists_phone_number(self, phone_number: str) -> User | None:
        """Проверка на существование номера телефона."""
        raise NotImplementedError("Метод должен быть реализован подклассами.")

    @abstractmethod
    async def is_exists_email(self, email: str) -> User | None:
        """Проверка на существование почты."""
        raise NotImplementedError("Метод должен быть реализован подклассами.")

    @abstractmethod
    async def is_exists_username(self, username: str) -> User | None:
        """Проверка на существование никнейма у пользователя."""
        raise NotImplementedError("Метод должен быть реализован подклассами.")
