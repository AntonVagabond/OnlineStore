# from typing import Optional, Union
# from uuid import UUID
#
# import pytest
# from common.const.response_exceptions import USER_NOT_FOUND
# from common.exceptions import mixins as exceptions
# from modules.schemas.admin_panels import UpdateAdminSchema, UserByRoleFilterSchema
# from modules.services.admin_panels import AdminPanelService
#
# from tests.unit.data import admin_panels as data_array
# from tests.unit.fixtures.admin_panels import AdminTestUOW
#
#
# @pytest.mark.parametrize(*data_array.GET_LIST_USERS_ADMIN_TEST_DATA)
# async def test_get_list_users_admin(
#     admin_panel_uow: AdminTestUOW,
#     admin_panel_service: AdminPanelService,
#     test_data: dict[str, Union[Optional[str], int]],
# ) -> None:
#     """Тестирование получения всех пользователей для администратора."""
#     count = test_data.pop("count")
#     response = await admin_panel_service.get_all(
#         admin_panel_uow, UserByRoleFilterSchema(**test_data)
#     )
#     assert len(response.records) == count
#
#
# @pytest.mark.parametrize(*data_array.GET_USER_TEST_DATA)
# async def test_get_user(
#     admin_panel_uow: AdminTestUOW,
#     admin_panel_service: AdminPanelService,
#     uuid: UUID,
#     test_result: bool,
# ) -> None:
#     """Тест для получения данных пользователя для редактирования."""
#     if test_result == USER_NOT_FOUND:
#         with pytest.raises(exceptions.UserNotFoundException) as exc:
#             await admin_panel_service.get(admin_panel_uow, uuid)
#         assert exc.value.detail == test_result
#     else:
#         user = await admin_panel_service.get(admin_panel_uow, uuid)
#         assert bool(user) == test_result
#
#
# @pytest.mark.parametrize(*data_array.UPDATE_USER_ADMIN_TEST_DATA)
# async def test_update_user_admin(
#     admin_panel_uow: AdminTestUOW,
#     admin_panel_service: AdminPanelService,
#     test_data: dict[str, Union[str, int]],
# ) -> None:
#     """Тестирование изменения пользователя для администратора."""
#     test_result = test_data.pop("test_result")
#     model = UpdateAdminSchema(**test_data)
#
#     if isinstance(test_result, str):
#         with pytest.raises(exceptions.UserNotFoundException) as exc:
#             await admin_panel_service.edit(admin_panel_uow, model)
#         assert exc.value.detail == test_result
#     else:
#         bool_result = await admin_panel_service.edit(admin_panel_uow, model)
#         assert bool_result == test_result
#
#
# @pytest.mark.parametrize(*data_array.DELETE_USER_TEST_DATA)
# async def test_delete_user(
#     admin_panel_uow: AdminTestUOW,
#     admin_panel_service: AdminPanelService,
#     uuid: UUID,
#     test_result: Union[bool, str],
# ) -> None:
#     """Тест для обновления статуса удаления пользователя."""
#     if test_result == USER_NOT_FOUND:
#         with pytest.raises(exceptions.UserNotFoundException) as exc:
#             await admin_panel_service.delete(admin_panel_uow, uuid)
#         assert exc.value.detail == test_result
#     else:
#         uuid_result = await admin_panel_service.delete(admin_panel_uow, uuid)
#         assert bool(uuid_result) == test_result
