from typing import Union, Optional
from uuid import UUID

import pytest
from fastapi import HTTPException

from common.enums.role import RoleEnum
from common.exceptions import mixins as exceptions
from modules.schemas.profiles import RegisterUserSchema
from modules.services.profiles import ProfileService
from tests.unit.data import profiles as data_array
from tests.unit.fixtures.profiles import ProfileTestUOW


@pytest.mark.parametrize(*data_array.GET_USER_INFO_TEST_DATA)
async def test_get_user_info(
        profile_uow: ProfileTestUOW,
        profile_service: ProfileService,
        user_id: str,
        test_result: bool,
) -> None:
    """Тест получения информации профиля пользователя."""
    if isinstance(test_result, str):
        with pytest.raises(exceptions.UserNotFoundException) as exc:
            await profile_service.get(profile_uow, UUID(user_id))
        assert exc.value.detail == test_result
    else:
        user = await profile_service.get(profile_uow, UUID(user_id))
        assert bool(user) == test_result


@pytest.mark.parametrize(*data_array.CREATE_USERS_PROFILE_TEST_DATA)
async def test_create_users_profile(
        profile_uow: ProfileTestUOW,
        profile_service: ProfileService,
        test_data: dict[str, Union[str, bool, Optional[int], RoleEnum]]
) -> None:
    """Тест для регистрации пользователя."""
    test_result = test_data.pop("test_result")
    filters = RegisterUserSchema(**test_data)

    list_exceptions = (
        exceptions.EmailAlreadyExistsException,
        exceptions.PhoneNumberAlreadyExistsException,
    )

    if isinstance(test_result, str):
        with pytest.raises(HTTPException) as exc:
            await profile_service.create(profile_uow, filters)
        assert exc.type in list_exceptions
        assert exc.value.detail == test_result
    else:
        result = await profile_service.create(profile_uow, filters)
        assert bool(result) == test_result
