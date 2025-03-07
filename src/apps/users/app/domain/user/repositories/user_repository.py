from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from ..entities.user import User


class UserRepository(Protocol):
    """Протокол для репозитория пользователей."""

    @abstractmethod
    def add(self, user: User) -> None:
        """Добавить пользователя."""
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        """Обновить данные пользователя."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: User) -> None:
        """Удалить пользователя по идентификатору."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
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
