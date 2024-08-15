import logging
from types import TracebackType
from typing import Self, TypeVar, Optional, Generic

from fastapi import HTTPException

from common.interfaces.abstraction_uow import IUnitOfWork
from common.repositories.base import BaseRepository
from core.database import async_session_maker

TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseUnitOfWork(IUnitOfWork):
    """Базовый класс для работы с транзакциями."""
    repo: Optional[TRepository]

    def __init__(self) -> None:
        self.__session_factory = async_session_maker

    async def __aenter__(self) -> Self:
        """Базовый метод входа в контекстного менеджера."""
        self._session = self.__session_factory()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        """Базовый метод выхода из контекстного менеджера"""
        if exc_type:
            await self.rollback()
            logging.error(
                {
                    "exception": exc_type,
                    "detail": exc_val.args[0] if exc_val.args else None,
                    "class": (
                        exc_tb.tb_next.tb_frame.f_locals["self"].__class__.__name__
                        if exc_tb.tb_next.tb_frame.f_locals.get("self") else
                        exc_tb.tb_next.tb_frame.f_locals["cls"].__name__
                    ),
                    "user_id": (
                        exc_tb.tb_frame.f_locals["user_uuid"].hex
                        if exc_tb.tb_frame.f_locals.get("user_uuid") else
                        None
                    )
                }
            )
            await self._session.close()
            raise HTTPException(status_code=500, detail=exc_val)
        await self._session.close()

    async def commit(self) -> None:
        """Базовый метод фиксирования транзакции."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Базовый метод завершения транзакции."""
        await self._session.rollback()