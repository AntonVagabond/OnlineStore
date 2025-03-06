from typing import TYPE_CHECKING

from dishka import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.presentation.api.schemas.base import SuccessfulResponse
from app.presentation.api.schemas.responses import user as responses

if TYPE_CHECKING:
    from uuid import UUID

    from app.application.user.commands.create_user import (
        CreateUserCommand,
        CreateUserHandler,
    )

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
