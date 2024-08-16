import logging
from types import TracebackType, NoneType
from typing import Self, TypeVar, Optional

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

        # Регистрируем и вызываем все кастомные исключения.
        if not isinstance(exc_type, (HTTPException, NoneType)):
            await self.rollback()
            logging.error(
                {
                    "exception": exc_val.__class__.__name__,
                    "detail": getattr(exc_val, "detail"),
                    "class": (
                        exc_tb.tb_next.tb_frame.f_locals["self"].__class__.__name__
                        if exc_tb.tb_next.tb_frame.f_locals.get("self") else
                        exc_tb.tb_next.tb_frame.f_locals["cls"].__name__
                    ) if exc_tb.tb_next else "Нет класса.",
                    "user_id": (
                        exc_tb.tb_frame.f_locals["user_uuid"].hex
                        if exc_tb.tb_frame.f_locals.get("user_uuid") else
                        "ID пользователя не найден."
                    )
                }
            )
            await self._session.close()
            raise exc_type()

        #  Регистрируем и вызываем не отслеживаемые исключения.
        if exc_type:
            await self.rollback()
            logging.error(
                {
                    "exception": exc_val.__class__.__name__,
                    "detail": getattr(exc_val, "detail"),
                    "class": (
                        exc_tb.tb_next.tb_frame.f_locals["self"].__class__.__name__
                        if exc_tb.tb_next.tb_frame.f_locals.get("self") else
                        exc_tb.tb_next.tb_frame.f_locals["cls"].__name__
                    ) if exc_tb.tb_next else "Нет класса.",
                    "user_id": (
                        exc_tb.tb_frame.f_locals["user_uuid"].hex
                        if exc_tb.tb_frame.f_locals.get("user_uuid") else
                        "ID пользователя не найден."
                    )
                }
            )
            await self._session.close()
            raise HTTPException(status_code=500, detail=getattr(exc_val, "detail"))
        await self._session.close()

    async def commit(self) -> None:
        """Базовый метод фиксирования транзакции."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Базовый метод завершения транзакции."""
        await self._session.rollback()
