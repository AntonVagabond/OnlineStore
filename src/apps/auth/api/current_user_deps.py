from datetime import datetime
from typing import Optional, Callable, Coroutine, Any, Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import MissingRequiredClaimError, DecodeError, ExpiredSignatureError

from core.config import get_settings
from core.security import Security
from modules.schemas.auth_schema import UserInfoSchema, AuthExceptionSchema
from modules.unit_of_works.auth_uow import AuthUOW

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=str(settings.auth.token_url), scheme_name="JWT",
)


class CurrentUserDep:
    """Зависимость для получения текущего пользователя."""
    @staticmethod
    async def get_data_user(
            roles: Optional[tuple[str, ...]],
            token: str,
    ) -> Union[UserInfoSchema, AuthExceptionSchema]:
        """Получить данные пользователя."""
        credentials_exception = {
            "status_code": 401,
            "detail": "Не удалось подтвердить учетные данные",
            "headers": {"WWW-Authenticate": "Bearer"},
        }
        try:
            payload = Security.decode_token(token)
        except ExpiredSignatureError:
            return AuthExceptionSchema(
                status_code=403,
                detail="Срок действия вашего токена истек. "
                       "Пожалуйста, войдите в систему еще раз."
            )
        except DecodeError:
            return AuthExceptionSchema(
                status_code=403,
                detail="Ошибка при расшифровке токена. "
                       "Пожалуйста, проверьте свой запрос."
            )
        except MissingRequiredClaimError:
            return AuthExceptionSchema(
                status_code=403,
                detail="В вашем токене нет обязательного поля. "
                       "Пожалуйста, свяжитесь с администратором."
            )

        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            return AuthExceptionSchema(**credentials_exception)
        email = payload.get("sub")
        if email is None:
            return AuthExceptionSchema(**credentials_exception)

        async with AuthUOW() as uow:
            data_user = await uow.repo.authenticate_user(email)

        if data_user is None:
            return AuthExceptionSchema(**credentials_exception)
        if data_user.deleted:
            return AuthExceptionSchema(status_code=400, detail="Удалённый пользователь")

        if roles:
            is_valid_role = any([req_role == data_user.role_name for req_role in roles])
            if not is_valid_role:
                return AuthExceptionSchema(
                    status_code=403,
                    detail=f"Для этого действия требуется одна из "
                           f"ролей: '{', '.join(req_role for req_role in roles)}'",
                )
        return data_user

    @classmethod
    def get_current_user(
            cls, roles: Optional[tuple[str, ...]] = None,
    ) -> Callable[[str], Coroutine[Any, Any, UserInfoSchema]]:
        """Возвращает авторизованного пользователя."""

        async def current_user(
                token: str = Depends(oauth2_scheme),
        ) -> Union[UserInfoSchema, AuthExceptionSchema]:
            """Поиск текущего пользователя."""
            response = await cls.get_data_user(token=token, roles=roles)
            if isinstance(response, AuthExceptionSchema):
                raise HTTPException(**response.model_dump())
            return response

        return current_user
