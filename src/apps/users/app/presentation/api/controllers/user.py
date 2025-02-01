from typing import TYPE_CHECKING

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.presentation.api.schemas.responses import SuccessfulResponse

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
    responses=...,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
    command: CreateUserCommand, handler: FromDishka[CreateUserHandler]
) -> SuccessfulResponse[UUID]:
    result = await handler.handle(command)
    return SuccessfulResponse(status.HTTP_201_CREATED, result)
