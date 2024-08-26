from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from common.repositories.base import BaseRepository
from models import Role
from models.users import User
from modules.schemas.auth_schema import UserInfoSchema


class AuthRepository(BaseRepository):
    """Репозиторий аутентификации."""
    model = User

    async def get_user_by_email(self, email: str) -> Optional[UserInfoSchema]:
        """Получить пользователя по почте."""
        result = await self.session.execute(
            sa.select(self.model)
            .options(joinedload(self.model.role).load_only(Role.name))
            .where(self.model.email == email)
        )
        user = result.scalar_one_or_none()
        return None if not user else UserInfoSchema(
            id=getattr(user.id, "hex"),
            email=user.email,
            deleted=user.deleted,
            password_hash=user.password_hash,
            role_name=user.role.name,
        )

    async def authenticate_user(self, email: str) -> Optional[UserInfoSchema]:
        """Аутентификация пользователя."""
        return await self.get_user_by_email(email)
