from typing import Self, Generic, TypeVar, Optional

from common.interfaces.abstraction_uow import IUnitOfWork
from common.repositories.base import BaseRepository
from core.database import async_session_maker

TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseUnitOfWork(IUnitOfWork, Generic[TRepository]):
    """Базовый класс для работы с транзакциями."""
    repo: Optional[TRepository]

    def __init__(self) -> None:
        self.__session_factory = async_session_maker
        self.init_repo: type[TRepository] = type(TRepository)

    async def __aenter__(self) -> Self:
        """Вход в контекстного менеджера."""
        self._session = self.__session_factory()
        self.repo = self.init_repo(self._session)
        return self

    async def __aexit__(self, *args) -> None:
        """Выход из контекстного менеджера"""
        await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        """Фиксирование транзакции."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Завершение транзакции."""
        await self._session.rollback()
