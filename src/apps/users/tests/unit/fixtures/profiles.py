# from types import TracebackType
# from typing import Optional
#
# import pytest
# from modules.services.profiles import ProfileService
# from modules.unit_of_works.profiles import ProfileUOW
#
#
# class ProfileTestUOW(ProfileUOW):
#     """Класс для тестирования профиля."""
#
#     async def __aexit__(
#         self,
#         exc_type: Optional[type[BaseException]],
#         exc_val: Optional[BaseException],
#         exc_tb: Optional[TracebackType],
#     ) -> None:
#         """Метод тестового класса выхода из контекстного менеджера"""
#         if exc_type is None:
#             await self.rollback()  # Откат изменений после каждого теста
#             await self.close()
#         else:
#             await super().__aexit__(exc_type, exc_val, exc_tb)
#
#     async def commit(self) -> None:
#         """Переопределение метода фиксирования транзакции."""
#         await self._session.flush()  # Сброс всех изменений в БД.
#
#
# @pytest.fixture(scope="function")
# async def profile_uow() -> ProfileTestUOW:
#     """Фикстура для работы с тестовыми транзакциями профиля."""
#     return ProfileTestUOW()
#
#
# @pytest.fixture(scope="function")
# async def profile_service() -> ProfileService:
#     """Фикстура для работы с профиля."""
#     return ProfileService()
