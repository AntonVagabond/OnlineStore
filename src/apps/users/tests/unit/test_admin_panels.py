from typing import Optional, Union

import pytest

from modules.schemas.admin_panels import UserByRoleFilterSchema
from modules.services.admin_panels import AdminPanelService
from modules.unit_of_works.admin_panels import AdminPanelUOW
from tests.unit.data.admin_panels import GET_LIST_USERS_ADMIN_TEST_DATA


@pytest.mark.parametrize(*GET_LIST_USERS_ADMIN_TEST_DATA)
async def test_get_list_users_admin(
        admin_panel_uow: AdminPanelUOW,
        admin_panel_service: AdminPanelService,
        test_data: dict[str, Union[Optional[str], int]]
) -> None:
    """Тестирование получения всех пользователей для администратора."""
    count = test_data.pop("count")
    response = await admin_panel_service.get_all(
        admin_panel_uow, UserByRoleFilterSchema(**test_data)
    )
    assert len(response.records) == count
