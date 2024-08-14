from __future__ import annotations

from typing import Self

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.profiles import ProfileRepository


class ProfileUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями профиля."""

    async def __aenter__(self) -> Self:
        """Метод входа в контекстного менеджера для профиля."""
        await super().__aenter__()
        self.repo = ProfileRepository(self._session)
        return self
