from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.application.common.dto.user_dto import UserDto


class UserReader(Protocol):
    """Протокол для чтения пользователей."""

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserDto | None:
        """Получить пользователя."""
        raise NotImplementedError
