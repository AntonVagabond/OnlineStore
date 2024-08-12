from __future__ import annotations

import logging
from types import TracebackType
from typing import Optional

from fastapi import HTTPException
from jwt import ExpiredSignatureError, DecodeError, MissingRequiredClaimError

from modules.repositories.auth_repository import AuthRepository
from common.unit_of_works.base import BaseUnitOfWork


class AuthUOW(BaseUnitOfWork):
    """Класс для работы с транзакциями аутентификации."""
    repo = AuthRepository

    async def __aenter__(self) -> AuthUOW:
        """Вход в контекстного менеджера."""
        await super().__aenter__()
        self.repo = AuthRepository(self._session)
        return self

    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера"""
        await self.rollback()
        if exc_type == ExpiredSignatureError:
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
            raise HTTPException(
                status_code=403,
                detail="Срок действия вашего токена истек. "
                       "Пожалуйста, войдите в систему еще раз."
            )
        if exc_type == DecodeError:
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
            raise HTTPException(
                status_code=403,
                detail="Ошибка при расшифровке токена. "
                       "Пожалуйста, проверьте свой запрос."
            )
        if exc_type == MissingRequiredClaimError:
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
            raise HTTPException(
                status_code=403,
                detail="В вашем токене нет обязательного поля. "
                       "Пожалуйста, свяжитесь с администратором."
            )
        await self._session.close()
