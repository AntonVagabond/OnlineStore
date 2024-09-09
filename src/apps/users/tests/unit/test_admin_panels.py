from typing import Optional, Union

import pytest

from common.exceptions import mixins as exceptions
from modules.schemas.admin_panels import UserByRoleFilterSchema, UpdateAdminSchema
from modules.services.admin_panels import AdminPanelService
from tests.unit.data.admin_panels import (
    GET_LIST_USERS_ADMIN_TEST_DATA, UPDATE_USER_ADMIN_TEST_DATA,
)
from tests.unit.fixtures.admin_panels import AdminTestUOW


@pytest.mark.parametrize(*GET_LIST_USERS_ADMIN_TEST_DATA)
async def test_get_list_users_admin(
        admin_panel_uow: AdminTestUOW,
        admin_panel_service: AdminPanelService,
        test_data: dict[str, Union[Optional[str], int]]
) -> None:
    """Тестирование получения всех пользователей для администратора."""
    count = test_data.pop("count")
    response = await admin_panel_service.get_all(
        admin_panel_uow, UserByRoleFilterSchema(**test_data)
    )
    assert len(response.records) == count


@pytest.mark.parametrize(*UPDATE_USER_ADMIN_TEST_DATA)
async def test_update_user_admin(
        admin_panel_uow: AdminTestUOW,
        admin_panel_service: AdminPanelService,
        test_data: dict[str, Union[str, int]]
) -> None:
    """Тестирование изменения пользователя для администратора."""
    test_result = test_data.pop("test_result")
    model = UpdateAdminSchema(**test_data)

    if isinstance(test_result, str):
        with pytest.raises(exceptions.UserNotFoundException) as exc:
            await admin_panel_service.edit(admin_panel_uow, model)
        assert exc.value.detail == test_result
    else:
        bool_result = await admin_panel_service.edit(admin_panel_uow, model)
        assert bool_result == test_result
