from types import TracebackType
from typing import Optional, Self

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

    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера"""
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.close()
