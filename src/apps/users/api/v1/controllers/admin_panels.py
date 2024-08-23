from fastapi import APIRouter

from api.dependencies import (
    AdminPanelUOWDep, AdminPanelServiceDep, UserByRoleFilterDep, AdminDep,
)
from common.schemas.internal.mixins import PageViewSchema
from modules.responses import admin_panels as responses
from modules.schemas.admin_panels import UserViewSchemaForAdminTable

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
