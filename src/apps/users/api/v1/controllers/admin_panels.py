from uuid import UUID

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from api.dependencies import (
    AdminDep,
    AdminPanelServiceDep,
    AdminPanelUOWDep,
    UserByRoleFilterDep,
)
from common.schemas.internal.mixins import PageViewSchema
from modules.responses import admin_panels as responses
from modules.schemas.admin_panels import (
    UpdateAdminSchema,
    UserResponseSchema,
    UserViewSchemaForAdminTable,
)

admin_panel = APIRouter(prefix="/api/v1/admin_panel", tags=["AdminPanel"])


@admin_panel.get(
    path="/",
    summary="Получение списка данных о пользователях (Admin).",
    responses=responses.GET_LIST_RESPONSES,
    dependencies=(AdminDep,),
)
async def get_list_users_admin(
    uow: AdminPanelUOWDep,
    service: AdminPanelServiceDep,
    filters: UserByRoleFilterDep,
) -> PageViewSchema[UserViewSchemaForAdminTable]:
    """Контроллер получения информации пользователей для admin-a."""
    user_list = await service.get_all(uow, filters)
    return user_list


@admin_panel.get(
    path="/edit/{user_id}/",
    summary="Получение данных о пользователя для редактирования (Admin).",
    responses=responses.GET_RESPONSES,
    dependencies=(AdminDep,),
)
async def get_user_admin(
    uow: AdminPanelUOWDep,
    service: AdminPanelServiceDep,
    user_id: UUID,
) -> UserResponseSchema:
    """Контроллер для получения данных пользователя для редактирования (admin)."""
    user = await service.get(uow, user_id)
    return user


@admin_panel.patch(
    path="/edit/",
    summary="Редактирование пользователя (Admin).",
    responses=responses.EDIT_RESPONSES,
    dependencies=(AdminDep,),
)
async def update_user_admin(
    uow: AdminPanelUOWDep,
    service: AdminPanelServiceDep,
    model: UpdateAdminSchema,
) -> Response:
    """Контроллер для редактирования пользователя."""
    bool_result = await service.edit(uow, model)
    return bool_result


@admin_panel.patch(
    path="/delete_user/{user_id}/",
    summary="Удаление пользователя (admin).",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.DELETE_RESPONSES,
    dependencies=(AdminDep,),
)
async def delete_user(
    uow: AdminPanelUOWDep,
    service: AdminPanelServiceDep,
    user_id: UUID,
) -> Response:
    """Контроллер для обновления статуса удаления пользователя."""
    await service.delete(uow, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
