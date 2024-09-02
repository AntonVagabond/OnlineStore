import pytest

from modules.services.profiles import ProfileService
from modules.unit_of_works.profiles import ProfileUOW


@pytest.fixture(scope="function")
async def profile_uow() -> ProfileUOW:
    """Фикстура для работы с тестовыми транзакциями профиля."""
    return ProfileUOW()


@pytest.fixture(scope="function")
async def profile_service() -> ProfileService:
    """Фикстура для работы с профиля."""
    return ProfileService()
