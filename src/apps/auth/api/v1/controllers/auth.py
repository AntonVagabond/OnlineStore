from typing import Union

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from ...dependencies import (
    OAuth2PasswordDep, AuthUOWDep, RefreshDep, UserDep, AuthUserServiceDep,
)
from modules.schemas.auth_schema import (
    TokenInfoSchema, LogoutResponseSchema, UserInfoSchema, AuthExceptionSchema,
)
from core.config import get_settings
from core.constants import REFRESH
from core.security import Security

settings = get_settings()

auth = APIRouter(prefix="/api/v1/Auth", tags=["Auth"])


@auth.post(
    path="/login/",
    summary="Вход в учетную запись.",
    responses={
        400: {"detail": "Некорректные данные"},
        401: {"detail": "Не авторизованный пользователь"},
        500: {"detail": "Ошибка сервера"},
    },
)
async def login_user(
        uow: AuthUOWDep,
        service: AuthUserServiceDep,
        form_data: OAuth2PasswordDep,
        response: Response
) -> TokenInfoSchema:
    """
    Контроллер для входа в учетную запись пользователя.

    Обязательные аргументы:
    * *`username`* *(email)* - ввод почты.

    * *`password`* - ввод пароля.
    """
    data_user = await service.get_user_for_create_tokens(uow, form_data)
    access_token = Security.create_access_token(data_user.email)
    refresh_token = Security.create_refresh_token(data_user.email)
    response.set_cookie(
        key=REFRESH,
        value=refresh_token,
        httponly=True,
        secure=True,
    )
    return TokenInfoSchema(access_token=access_token)


@auth.post(path="/refresh/", status_code=201)
async def get_new_access_token(
        uow: AuthUOWDep,
        service: AuthUserServiceDep,
        response: Response,
        refresh: RefreshDep,
) -> TokenInfoSchema:
    """
    Контроллер для обновления токена доступа.

    Аргументы:
    * *`refresh_token`* - токен обновления (*скрытый*).
    """
    user_info = await service.get_user_for_update_tokens(uow, refresh)
    access_token = Security.create_access_token(user_info.email)
    refresh_token = Security.create_refresh_token(user_info.email)
    response.set_cookie(
        key=REFRESH,
        value=refresh_token,
        httponly=True,
        secure=True,
    )
    return TokenInfoSchema(access_token=access_token)


@auth.post(path="/logout/", dependencies=UserDep)
async def logout_user(
        response: Response
) -> LogoutResponseSchema:
    """Контроллер для выхода из учетной записи."""
    response.delete_cookie(REFRESH, httponly=True, secure=True)
    return LogoutResponseSchema()


@auth.get(path="/authenticate/")
async def auth_user(
        request: Request, service: AuthUserServiceDep,
) -> Union[UserInfoSchema, AuthExceptionSchema]:
    """Контроллер для аутентификации пользователя."""
    headers = request.headers
    access_token = headers.get("access_token")
    if roles := headers.get("roles") is not None:
        roles = tuple(headers.get("roles").split(", "))
    response = await service.get_data_user(access_token, roles)
    return response
