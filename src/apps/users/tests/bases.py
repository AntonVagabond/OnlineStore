from types import TracebackType
from typing import Optional

from common.unit_of_works.base import BaseUnitOfWork


class TestUnitOfWork(BaseUnitOfWork):
    """Класс для тестирования базового UnitOfWork."""

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
