import json
import logging
from types import TracebackType
from typing import Optional, Self, TypeVar

from fastapi import HTTPException
from redis.asyncio import Redis

from common.interfaces.abstraction_uow import IUnitOfWork
from common.repositories.base import BaseRepository
from core.database import redis_engine

TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseUnitOfWork(IUnitOfWork):
    """Базовый класс для работы с транзакциями."""

    repo: Optional[TRepository]

    def __init__(self) -> None:
        self.__session_factory = redis_engine
        self._session: Optional[Redis] = None

    async def __aenter__(self) -> Self:
        """Вход в контекстного менеджера."""
        self._session = self.__session_factory.client()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера"""

        # Регистрируем и вызываем все кастомные исключения.
        if exc_type is not None and exc_type.__base__ == HTTPException:
            logging.exception(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "status_code": getattr(exc_val, "status_code"),
                        "detail": getattr(exc_val, "detail"),
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise exc_val

        #  Регистрируем и вызываем не отслеживаемые исключения.
        if exc_type:
            detail_massage = (
                getattr(exc_val, "detail")
                if getattr(exc_val, "detail", None)
                else exc_val.args[0] if exc_val.args else None
            )
            logging.error(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "status_code": 500,
                        "detail": detail_massage,
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise HTTPException(status_code=500, detail=detail_massage)
        await self.close()

    async def close(self) -> None:
        """Базовый метод закрытия транзакции."""
        await self._session.aclose()
