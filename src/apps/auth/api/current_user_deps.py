from datetime import datetime
from typing import Any, Callable, Coroutine, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError

from common.const import mixins as resp_exc
from common.exceptions import mixins as error
from core.config import settings
from core.security import Security
from modules.schemas.auth_schema import UserInfoSchema
from modules.unit_of_works.auth_uow import AuthUOW

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=str(settings.auth.token_url),
    scheme_name="JWT",
)


class CurrentUserDep:
    """Зависимость для получения текущего пользователя."""

    @staticmethod
    async def get_data_user(
        roles: Optional[tuple[str, ...]], token: str
    ) -> UserInfoSchema:
        """Получить данные пользователя."""
        try:
            payload = Security.decode_token(token)
        except ExpiredSignatureError:
            raise error.AuthForbiddenException(detail=resp_exc.TOKEN_EXPIRED_FORBIDDEN)
        except DecodeError:
            raise error.AuthForbiddenException(detail=resp_exc.TOKEN_INVALID_FORBIDDEN)
        except MissingRequiredClaimError:
            raise error.AuthForbiddenException(
                detail=resp_exc.TOKEN_REQUIRED_FIELD_FORBIDDEN,
            )

        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise error.AuthUnauthorizedException()
        email = payload.get("sub")
        if email is None:
            raise error.AuthUnauthorizedException()

        async with AuthUOW() as uow:
            data_user = await uow.repo.authenticate_user(email)

        if data_user is None:
            raise error.AuthUnauthorizedException()
        if data_user.deleted:
            raise error.AuthBadRequestException(detail=resp_exc.USER_BAD_REQUEST)

        if roles:
            is_valid_role = any([req_role == data_user.role_name for req_role in roles])
            if not is_valid_role:
                raise error.AuthForbiddenException(
                    detail=f"Для этого действия требуется одна из "
                    f"ролей: '{', '.join(req_role for req_role in roles)}'.",
                )
        return data_user

    @classmethod
    def get_current_user(
        cls, roles: Optional[tuple[str, ...]] = None
    ) -> Callable[[str], Coroutine[Any, Any, UserInfoSchema]]:
        """Возвращает авторизованного пользователя."""

        async def current_user(
            token: str = Depends(oauth2_scheme),
        ) -> UserInfoSchema:
            """Поиск текущего пользователя."""
            response = await cls.get_data_user(token=token, roles=roles)
            return response

        return current_user
