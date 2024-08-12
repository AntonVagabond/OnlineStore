from typing import Optional

import sqlalchemy as sa

from common.repositories.base import BaseRepository
from models.users import User
from modules.schemas.auth_schema import UserInfoSchema


class AuthRepository(BaseRepository[User]):
    """Репозиторий аутентификации."""

    async def get_user_by_email(self, email: str) -> Optional[UserInfoSchema]:
        """Получить пользователя по почте."""
        result = await self.session.execute(
            sa.select(self.model)
            .filter(
                self.model.email == email,
                self.model.deleted.__eq__(False),
                self.model.logged_out.__eq__(False),
            )
        )
        user = result.scalar_one_or_none()
        return None if not user else UserInfoSchema(
            id=getattr(user.id, "hex"),
            email=user.email,
        )

    async def authenticate_user(self, email: str) -> Optional[UserInfoSchema]:
        """Аутентификация пользователя."""
        return await self.get_user_by_email(email)
