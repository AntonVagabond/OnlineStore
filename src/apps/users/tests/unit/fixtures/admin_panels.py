import pytest

from modules.services.admin_panels import AdminPanelService
from modules.unit_of_works.admin_panels import AdminPanelUOW


@pytest.fixture(scope="function")
async def admin_panel_uow() -> AdminPanelUOW:
    """Фикстура для работы с тестовыми транзакциями панели администратора."""
    return AdminPanelUOW()


@pytest.fixture(scope="function")
async def admin_panel_service() -> AdminPanelService:
    """Фикстура для работы с сервисом панели администратора."""
    return AdminPanelService()
