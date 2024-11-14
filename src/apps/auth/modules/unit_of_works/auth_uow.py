from typing import Self

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.auth_repository import AuthRepository


class AuthUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями аутентификации."""

    repo = AuthRepository

    async def __aenter__(self) -> Self:
        """Вход в контекстного менеджера."""
        await super().__aenter__()
        self.repo = AuthRepository(self._session)
        return self
