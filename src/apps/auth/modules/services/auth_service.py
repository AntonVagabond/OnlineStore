from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from api.current_user_deps import CurrentUserDep
from common.const import mixins as resp_exc
from common.exceptions.mixins import AuthBadRequestException
from core.security import Security
from modules.schemas.auth_schema import UserInfoSchema
from modules.unit_of_works.auth_uow import AuthUOW


class AuthUserService:
    """Сервис для работы аутентификации."""

    @staticmethod
    async def get_user_for_create_tokens(
        uow: AuthUOW, form_data: OAuth2PasswordRequestForm
    ) -> UserInfoSchema:
        """Получить пользователя для создания токенов."""
        async with uow:
            data_user = await uow.repo.authenticate_user(form_data.username)
            if not data_user:
                raise AuthBadRequestException(detail=resp_exc.EMAIL_BAD_REQUEST)
            if not Security.verify_password(
                form_data.password, hashed_password=data_user.password_hash
            ):
                raise AuthBadRequestException(detail=resp_exc.PASSWORD_BAD_REQUEST)
            if data_user.deleted:
                raise AuthBadRequestException(detail=resp_exc.USER_BAD_REQUEST)
            return data_user

    @staticmethod
    async def get_user_for_update_tokens(
        uow: AuthUOW, refresh_token: str
    ) -> UserInfoSchema:
        """Получить пользователя для обновления токенов."""
        async with uow:
            payload = Security.decode_token(refresh_token)

            if payload["type"] == "refresh":
                email = payload["sub"]

                data_user = await uow.repo.authenticate_user(email)

                if data_user.deleted:
                    raise AuthBadRequestException(detail=resp_exc.USER_BAD_REQUEST)
                return data_user
            else:
                raise AuthBadRequestException(detail=resp_exc.TOKEN_BAD_REQUEST)

    @staticmethod
    async def get_data_user(
        token: str, roles: Optional[tuple[str, ...]]
    ) -> UserInfoSchema:
        """Получить данные текущего пользователя."""
        data_user = await CurrentUserDep.get_data_user(roles, token)
        return data_user
