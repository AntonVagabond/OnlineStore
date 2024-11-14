from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from api.dependencies import ProfileServiceDep, ProfileUOWDep, UserSchemaDep
from modules.responses import profiles as responses
from modules.schemas.profiles import (
    RegisterUserSchema,
    UpdateUserSchema,
    UserForAuthResponseSchema,
)

profile = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@profile.post(
    path="/register/",
    summary="Регистрация пользователя.",
    responses=responses.REGISTRATION_RESPONSES,
)
async def create_user(
    uow: ProfileUOWDep,
    service: ProfileServiceDep,
    model: RegisterUserSchema,
) -> Response:
    """Контроллер регистрации пользователя."""
    user_id = await service.create(uow, model)
    return user_id


@profile.get(
    path="/",
    summary="Получение профиля пользователя.",
    responses=responses.GET_RESPONSES,
)
async def get_user(
    current_user: UserSchemaDep, uow: ProfileUOWDep, service: ProfileServiceDep
) -> Response:
    """Контроллер получения информации профиля пользователя."""
    profile_data = await service.get(uow, current_user.id)
    return profile_data


@profile.patch(
    path="/edit/",
    summary="Редактирование профиля пользователя.",
    responses=responses.EDIT_RESPONSES,
)
async def update_user(
    current_user: UserSchemaDep,
    uow: ProfileUOWDep,
    service: ProfileServiceDep,
    model: UpdateUserSchema,
) -> Response:
    """Контроллер редактирования профиля пользователя."""
    bool_result = await service.update(uow, model, current_user.id)
    return bool_result


@profile.get(
    path="/user_for_auth/",
    include_in_schema=False,
    summary="Скрытый контроллер для получения данных микросервису Auth по httpx.",
)
async def auth_user(
    uow: ProfileUOWDep, request: Request, service: ProfileServiceDep
) -> UserForAuthResponseSchema:
    """Контроллер для аутентификации пользователя (скрытый)."""
    headers = request.headers
    username = headers.get("username")
    result = await service.get_user_for_auth(uow, username)
    return result
