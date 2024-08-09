import logging

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from api.dependencies import UserDep, ProfileUOWDep, ProfileServiceDep
from common.schemas.responses import mixins as responses

profile = APIRouter(prefix="/api/v1/Profile", tags=["Profile"])


@profile.get(
    path="/",
    dependencies=...,
    summary="Получение профиля пользователя",
    response_model=...,
    responses={
        status.HTTP_401_UNAUTHORIZED: responses.UnauthorizedResponseSchema().model_dump(),
        status.HTTP_403_FORBIDDEN: responses.ForbiddenResponseSchema().model_dump(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: responses.ServerErrorResponseSchema().model_dump(),
    },
)
async def get_user_info(
        current_user: UserDep, uow: ProfileUOWDep, service: ProfileServiceDep,
):
    """Контроллер получения информации профиля пользователя."""
    result = await service.get(uow, current_user.id)
    if result:
        return result
    logging.error(
        {
            "method": "get_user_info",
            "endpoint": "/",
            "status_code": 404,
            "message": "Пользователь не найден",
        }
    )
    return JSONResponse(
        status_code=404, content={"message": "Пользователь не найден"},
    )
