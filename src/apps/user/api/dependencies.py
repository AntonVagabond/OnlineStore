from typing import Annotated, Optional, Callable, Coroutine, Any
from uuid import UUID

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from common.schemas.api.mixins import CurrentUserSchema
from core.config import get_settings
from modules.services.profiles import ProfileService
from modules.unit_of_works.profiles import ProfileUOW

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=str(settings.token_url), scheme_name="JWT",
)


# region ------------------------------------- USER --------------------------------------
def get_current_user(
        roles: Optional[tuple[str, ...]] = None,
) -> Callable[[str], Coroutine[Any, Any, CurrentUserSchema]]:
    """Возвращает авторизованного пользователя."""

    async def current_user(token: str = Depends(oauth2_scheme)) -> CurrentUserSchema:
        """Поиск текущего пользователя."""
        async with httpx.AsyncClient() as client:
            data = {"access_token": token, "roles": roles}
            filter_data = dict(filter(lambda x: x[1] is not None, data.items()))
            if filter_data.get("roles") is not None:
                filter_data["roles"] = ', '.join(filter_data["roles"])  # noqa

            response = await client.get(
                url=str(settings.authenticate_url), headers=filter_data,
            )

            user_data_or_exc = response.json()
            if bool(user_data_or_exc.get("status_code")):
                raise HTTPException(
                    status_code=user_data_or_exc["status_code"],
                    detail=user_data_or_exc["detail"],
                    headers=user_data_or_exc["headers"],
                )
            return CurrentUserSchema(id=UUID(user_data_or_exc["id"]))

    return current_user


# endregion ------------------------------------------------------------------------------


# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[CurrentUserSchema, Depends(get_current_user())]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- PROFILE ---------------------------------------
ProfileUOWDep = Annotated[ProfileUOW, Depends(ProfileUOW)]
ProfileServiceDep = Annotated[ProfileService, Depends(ProfileService)]
# endregion ------------------------------------------------------------------------------
