import json
import logging
from types import TracebackType
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
        if exc_type is not None and exc_type.__base__ == HTTPException:
            await self.rollback()
            logging.exception(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "detail": getattr(exc_val, "detail"),
                        "class": (
                            (
                                exc_tb.tb_next.tb_frame.f_locals[
                                    "self"
                                ].__class__.__name__
                                if exc_tb.tb_next.tb_frame.f_locals.get("self")
                                else exc_tb.tb_next.tb_frame.f_locals["cls"].__name__
                            )
                            if exc_tb.tb_next
                            else "Нет класса."
                        ),
                        "user_id": (
                            exc_tb.tb_frame.f_locals["user_uuid"].hex
                            if exc_tb.tb_frame.f_locals.get("user_uuid")
                            else "ID пользователя не найден."
                        ),
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise exc_type()

        #  Регистрируем и вызываем не отслеживаемые исключения.
        if exc_type:
            await self.rollback()
            detail_massage = (
                getattr(exc_val, "detail")
                if getattr(exc_val, "detail", None)
                else exc_val.args[0] if exc_val.args else None
            )
            logging.error(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "detail": detail_massage,
                        "class": (
                            (
                                exc_tb.tb_next.tb_frame.f_locals[
                                    "self"
                                ].__class__.__name__
                                if exc_tb.tb_next.tb_frame.f_locals.get("self")
                                else exc_tb.tb_next.tb_frame.f_locals["cls"].__name__
                            )
                            if exc_tb.tb_next
                            else "Нет класса."
                        ),
                        "user_id": (
                            exc_tb.tb_frame.f_locals["user_uuid"].hex
                            if exc_tb.tb_frame.f_locals.get("user_uuid")
                            else "ID пользователя не найден."
                        ),
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise HTTPException(status_code=500, detail=detail_massage)

    async def commit(self) -> None:
        """Базовый метод фиксирования транзакции."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Базовый метод отмены транзакции."""
        await self._session.rollback()

    async def close(self) -> None:
        """Базовый метод закрытия транзакции."""
        await self._session.close()
