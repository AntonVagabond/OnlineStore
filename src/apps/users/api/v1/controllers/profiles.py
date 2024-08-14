import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse, Response

from api.dependencies import UserDep, ProfileUOWDep, ProfileServiceDep
from common.schemas.api.mixins import RegisterSchema
from common.schemas.responses import mixins as response
from modules.schemas.profiles import ProfileResponseSchema

profile = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@profile.post(
    path="/register/",
    summary="Регистрация пользователя.",
    responses={
        # 200: {"model": response.SuccessResponseSchema},
        400: {"model": response.BadRequestResponseSchema},
        401: {"model": response.UnauthorizedResponseSchema},
        403: {"model": response.ForbiddenResponseSchema},
        500: {"model": response.ServerErrorResponseSchema},
    }
)
async def create_user(
        current_user: UserDep,  # noqa
        uow: ProfileUOWDep,
        service: ProfileServiceDep,
        model: RegisterSchema,
) -> Response:
    """Контроллер регистрации пользователя."""
    result = await service.add(uow, model)
    if isinstance(result, str):
        return JSONResponse(status_code=400, content={"message": result})
    logging.info(
        {
            "method": "create_user",
            "endpoint": "/register/",
            "status_code": 200,
            "message": "Пользователь успешно создан",
        }
    )
    return JSONResponse(status_code=200, content={"message": "Пользователь успешно создан"})


@profile.get(
    path="/",
    summary="Получение профиля пользователя",
    responses={
        200: {"model": ProfileResponseSchema},
        401: {"model": response.UnauthorizedResponseSchema},
        403: {"model": response.ForbiddenResponseSchema},
        404: {"model": response.NotFoundResponseSchema},
        500: {"model": response.ServerErrorResponseSchema},
    },
)
async def get_user(
        current_user: UserDep, uow: ProfileUOWDep, service: ProfileServiceDep,
) -> Response:
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
