from fastapi import APIRouter
from starlette.responses import Response

from api.dependencies import UserDep, ProfileUOWDep, ProfileServiceDep
from common.schemas.api.mixins import RegisterSchema
from modules.responses import profiles as responses

profile = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@profile.post(
    path="/register/",
    summary="Регистрация пользователя.",
    responses=responses.REGISTRATION_RESPONSES,
)
async def create_user(
        current_user: UserDep,  # noqa
        uow: ProfileUOWDep,
        service: ProfileServiceDep,
        model: RegisterSchema,
) -> Response:
    """Контроллер регистрации пользователя."""
    user_id = await service.create(uow, model)
    return user_id


@profile.get(
    path="/",
    summary="Получение профиля пользователя",
    responses=responses.GET_RESPONSES,
)
async def get_user(
        current_user: UserDep, uow: ProfileUOWDep, service: ProfileServiceDep,
) -> Response:
    """Контроллер получения информации профиля пользователя."""
    profile_data = await service.get(uow, current_user.id)
    return profile_data
