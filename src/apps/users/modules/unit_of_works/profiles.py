from __future__ import annotations

from types import TracebackType
from typing import Self, Optional

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.profiles import ProfileRepository


class ProfileUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями профиля."""

    async def __aenter__(self) -> Self:
        """Метод входа в контекстного менеджера для профиля."""
        await super().__aenter__()
        self.repo = ProfileRepository(self._session)
        return self

    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера для профиля."""
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.close()
