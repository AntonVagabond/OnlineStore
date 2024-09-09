from fastapi import APIRouter
from starlette.responses import Response

from api.dependencies import (
    AdminPanelUOWDep, AdminPanelServiceDep, UserByRoleFilterDep, AdminDep,
)
from common.schemas.internal.mixins import PageViewSchema
from modules.responses import admin_panels as responses
from modules.schemas.admin_panels import UserViewSchemaForAdminTable, UpdateAdminSchema

admin_panel = APIRouter(prefix="/api/v1/admin_panel", tags=["AdminPanel"])


@admin_panel.get(
    path="/",
    summary="Получение списка данных о пользователях (Admin).",
    responses=responses.GET_LIST_RESPONSES,
    dependencies=(AdminDep,)
)
async def get_list_users_admin(
        uow: AdminPanelUOWDep,
        service: AdminPanelServiceDep,
        filters: UserByRoleFilterDep,
) -> PageViewSchema[UserViewSchemaForAdminTable]:
    """Контроллер получения информации пользователей для admin-a."""
    user_list = await service.get_all(uow, filters)
    return user_list


@admin_panel.patch(
    path="/edit/",
    summary="Редактирование пользователя (Admin).",
    responses=responses.EDIT_RESPONSES,
    dependencies=(AdminDep,)
)
async def update_user_admin(
        uow: AdminPanelUOWDep,
        service: AdminPanelServiceDep,
        model: UpdateAdminSchema,
) -> Response:
    """Контроллер для редактирования пользователя."""
    bool_result = await service.edit(uow, model)
    return bool_result
