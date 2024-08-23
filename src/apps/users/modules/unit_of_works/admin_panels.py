from typing import Self
from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.admin_panels import AdminPanelRepository


class AdminPanelUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями панели администратора."""
    repo = AdminPanelRepository

    async def __aenter__(self) -> Self:
        """Вход в контекстного менеджера."""
        await super().__aenter__()
        self.repo = AdminPanelRepository(self._session)
        return self
