from typing import Union, Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.current_user_deps import CurrentUserDep
from modules.schemas.auth_schema import UserInfoSchema, AuthExceptionSchema
from modules.unit_of_works.auth_uow import AuthUOW
from core.security import Security


class AuthUserService:
    """Сервис для работы аутентификации."""

    @staticmethod
    async def get_user_for_create_tokens(
            uow: AuthUOW, form_data: OAuth2PasswordRequestForm,
    ) -> UserInfoSchema:
        """Получить пользователя для создания токенов."""
        async with uow:
            data_user = await uow.repo.authenticate_user(form_data.username)
            if not data_user:
                raise HTTPException(
                    status_code=400,
                    detail="Неверный адрес электронной почты",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if not Security.verify_password(
                    form_data.password, hashed_password=data_user.password_hash
            ):
                raise HTTPException(status_code=400, detail="Неверный пароль")
            if data_user.deleted:
                raise HTTPException(status_code=400, detail="Пользователь удален")
            return data_user

    @staticmethod
    async def get_user_for_update_tokens(
            uow: AuthUOW, refresh_token: str,
    ) -> UserInfoSchema:
        """Получить пользователя для обновления токенов."""
        async with uow:
            payload = Security.decode_token(refresh_token)

            if payload["type"] == "refresh":
                email = payload["sub"]

                data_user = await uow.repo.authenticate_user(email)

                if data_user.deleted:
                    raise HTTPException(
                        status_code=400, detail="Пользователь удален",
                    )
                return data_user
            else:
                raise HTTPException(status_code=400, detail="Неверный токен")

    @staticmethod
    async def get_data_user(
            token: str, roles: Optional[tuple[str, ...]]
    ) -> Union[UserInfoSchema, AuthExceptionSchema]:
        """Получить данные текущего пользователя."""
        data_user = await CurrentUserDep.get_data_user(roles, token)
        return data_user
