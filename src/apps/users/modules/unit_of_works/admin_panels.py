from types import TracebackType
from typing import Self, Optional
from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.admin_panels import AdminPanelRepository


class AdminPanelUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями панели администратора."""

    repo = AdminPanelRepository

    async def __aenter__(self) -> Self:
        """Вход в контекстного менеджера для панели администратора."""
        await super().__aenter__()
        self.repo = AdminPanelRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера для панели администратора."""
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.close()
