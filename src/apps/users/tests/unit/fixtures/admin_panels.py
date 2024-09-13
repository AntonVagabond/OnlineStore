from types import TracebackType
from typing import Optional

import pytest

from modules.services.admin_panels import AdminPanelService
from modules.unit_of_works.admin_panels import AdminPanelUOW


class AdminTestUOW(AdminPanelUOW):
    """Класс для тестирования админ панели."""

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Метод тестового класса выхода из контекстного менеджера"""
        if exc_type is None:
            await self.rollback()  # Откат изменений после каждого теста
            await self.close()
        else:
            await super().__aexit__(exc_type, exc_val, exc_tb)

    async def commit(self) -> None:
        """Переопределение метода фиксирования транзакции."""
        await self._session.flush()  # Сброс всех изменений в БД.


@pytest.fixture(scope="function")
async def admin_panel_uow() -> AdminTestUOW:
    """Фикстура для работы с тестовыми транзакциями панели администратора."""
    return AdminTestUOW()


@pytest.fixture(scope="function")
async def admin_panel_service() -> AdminPanelService:
    """Фикстура для работы с сервисом панели администратора."""
    return AdminPanelService()
