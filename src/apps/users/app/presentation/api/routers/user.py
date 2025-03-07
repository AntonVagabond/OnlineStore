from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.application.common.dto.user_dto import UserDto
from app.application.user.commands.create_user import CreateUserCommand, CreateUserHandler
from app.application.user.queries.get_user import GetUserHandler, GetUserQuery
from app.presentation.api.schemas.base import SuccessfulResponse
from app.presentation.api.schemas.responses import user as responses

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post(
    path="/create",
    summary="Регистрация пользователя.",
    responses=responses.CREATE_USER_RESPONSES,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
    command: CreateUserCommand, handler: Depends[CreateUserHandler]
) -> SuccessfulResponse[UUID]:
    result = await handler.handle(command)
    return SuccessfulResponse(status.HTTP_201_CREATED, result)


@router.get(
    path="/{user_id}",
    summary="Получить пользователя по user_id.",
    responses=responses.GET_USER_RESPONSES,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user(
    user_id: UUID, handler: Depends[GetUserHandler]
) -> SuccessfulResponse[UserDto]:
    query = GetUserQuery(user_id)
    user = await handler.handle(query)
    return SuccessfulResponse(status.HTTP_200_OK, user)
