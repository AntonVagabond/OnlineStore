from datetime import timedelta, datetime
from typing import Any

import bcrypt
import jwt

from core.config import get_settings

settings = get_settings()


class Security:
    """Класс для работы с безопасностью."""

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        """Сравнивает хэшированный пароль с паролем из БД."""
        return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)

    @staticmethod
    def __create_token(payload: dict[str, Any], minutes: int) -> str:
        """Создание токена."""
        to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=minutes)

        to_encode.update(exp=expire, iat=now)
        return jwt.encode(
            payload=to_encode,
            key=settings.auth.private_key_path.read_text(),
            algorithm=settings.auth.algorithm,
        )

    @classmethod
    def create_access_token(cls, email: str) -> str:
        """Создать access токен."""
        payload = {"sub": email, "type": "access"}
        access_token = cls.__create_token(
            payload=payload, minutes=settings.auth.access_token_expire_minutes,
        )
        return access_token

    @classmethod
    def create_refresh_token(cls, email: str) -> str:
        """Создать refresh токен."""
        payload = {"sub": email, "type": "refresh"}
        refresh_token = cls.__create_token(
            payload=payload, minutes=settings.auth.refresh_token_expire_minutes,
        )
        return refresh_token

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Расшифровать токен."""
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.public_key_path.read_text(),
            algorithms=[settings.auth.algorithm])
        return payload
