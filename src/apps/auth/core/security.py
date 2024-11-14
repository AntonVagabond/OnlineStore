import datetime as dt
from typing import Any

import bcrypt
import jwt

from .config import settings


class Security:
    """Класс для работы с безопасностью."""

    @classmethod
    def verify_password(cls, password: str, hashed_password: bytes) -> bool:
        """Сравнивает хэшированный пароль с паролем из БД."""
        return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)

    @staticmethod
    def __create_token(payload: dict[str, Any], minutes: int, now: dt.datetime) -> str:
        """Создание токена."""
        to_encode = payload.copy()
        expire = now + dt.timedelta(minutes=minutes)

        to_encode.update(exp=expire, iat=now)
        return jwt.encode(
            payload=to_encode,
            key=settings.auth.private_key_path.read_text(),
            algorithm=settings.auth.algorithm,
        )

    @classmethod
    def create_access_token(cls, email: str, now: dt.datetime) -> str:
        """Создать access токен."""
        payload = {"sub": email, "type": "access"}
        access_token = cls.__create_token(
            payload=payload,
            minutes=settings.auth.access_token_expire_minutes,
            now=now,
        )
        return access_token

    @classmethod
    def create_refresh_token(cls, email: str, now: dt.datetime) -> str:
        """Создать refresh токен."""
        payload = {"sub": email, "type": "refresh"}
        refresh_token = cls.__create_token(
            payload=payload,
            minutes=settings.auth.refresh_token_expire_minutes,
            now=now,
        )
        return refresh_token

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Расшифровать токен."""
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.public_key_path.read_text(),
            algorithms=[settings.auth.algorithm],
        )
        return payload

    @staticmethod
    def decode_token_not_verify_signature(token: str) -> dict[str, Any]:
        """Расшифровать токен без проверки подписи."""
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.public_key_path.read_text(),
            algorithms=[settings.auth.algorithm],
            options={"verify_signature": False},
        )
        return payload
