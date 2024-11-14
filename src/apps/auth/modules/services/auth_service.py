import datetime as dt
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError

from api.current_user_deps import CurrentUserDep
from clients.users import UserClientService
from common.const import mixins as resp_exc
from common.exceptions import mixins as error
from common.exceptions.mixins import AuthBadRequestException, AuthNotFoundException
from core.config import settings
from core.security import Security
from modules.schemas.auth_schema import UserInfoSchema
from modules.unit_of_works.auth_uow import AuthUOW


class AuthUserService:
    """Сервис для работы аутентификации."""

    @staticmethod
    def __create_expire_device(now: dt.datetime) -> str:
        """Создание даты истечения срока девайса."""
        expire_device = now + dt.timedelta(settings.auth.refresh_token_expire_minutes)
        return dt.datetime.strftime(expire_device, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def __is_verify_password_and_user_not_deleted(
        password: str,
        hash_password: bytes,
        is_user_deleted: bool,
    ):
        """Проверка нового со старым паролем и проверка пользователя на его удаление."""
        if not Security.verify_password(password, hashed_password=hash_password):
            raise AuthBadRequestException(detail=resp_exc.PASSWORD_BAD_REQUEST)
        if is_user_deleted:
            raise AuthBadRequestException(detail=resp_exc.USER_BAD_REQUEST)

    @staticmethod
    def __change_data(data: dict[str, ...]) -> dict[str:...]:
        """Изменение данных."""
        data.update(deleted="1" if data["deleted"] else "0")
        # Удаляем данные значение None, так как Redis не принимает такие значения.
        return filter(lambda x: x[1] is not None, data.items())

    async def get_user_for_create_tokens(
        self,
        uow: AuthUOW,
        client: UserClientService,
        form_data: OAuth2PasswordRequestForm,
    ) -> tuple[str, dt.datetime]:
        """Получить пользователя для создания токенов."""
        async with uow:
            data_user = await uow.repo.get_user_for_authorization(form_data.username)

            now = dt.datetime.now(dt.timezone.utc)
            expire_device = self.__create_expire_device(now=now)

            if data_user is None:
                data_user = await client.get_user_over_httpx(username=form_data.username)

            if data_user is None:
                raise AuthNotFoundException(detail=resp_exc.USER_NOT_FOUND)

            if isinstance(data_user, list):
                login = data_user[0]
                hash_password = bytes(data_user[1], encoding="utf-8")
                deleted = True if data_user[2] == "1" else False
                expire_devices = data_user[3]
            else:
                login = data_user["email"]
                hash_password = bytes(data_user["hash_password"], encoding="utf-8")
                deleted = data_user["deleted"]

            self.__is_verify_password_and_user_not_deleted(
                form_data.password, hash_password, deleted
            )

            if isinstance(data_user, dict):
                gen_change_data = self.__change_data(data=data_user)
                data_for_redis = {k: v for k, v in gen_change_data}
                data_for_redis.update(expire_devices=expire_device)
            else:
                data_for_redis = {"login": login}
                data_for_redis.update(expire_devices=f"{expire_devices},{expire_device}")

            await uow.repo.set_user(data=data_for_redis)
            return login, now

    @staticmethod
    async def get_user_for_update_tokens(
        uow: AuthUOW, refresh_token: str
    ) -> tuple[str, dt.datetime]:
        """Получить пользователя для обновления токенов."""
        async with uow:
            try:
                payload = Security.decode_token(refresh_token)
            except ExpiredSignatureError:

                payload = Security.decode_token_not_verify_signature(refresh_token)
                login, expire = payload["sub"], payload["exp"]
                expire_timestamp = dt.datetime.fromtimestamp(expire, dt.timezone.utc)
                await uow.repo.delete_expire_device(login, expire_timestamp)

                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_EXPIRED_FORBIDDEN
                )
            except DecodeError:
                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_INVALID_FORBIDDEN
                )
            except MissingRequiredClaimError:
                raise error.AuthForbiddenException(
                    detail=resp_exc.TOKEN_REQUIRED_FIELD_FORBIDDEN,
                )

            if payload["type"] == "refresh":
                login = payload["sub"]
                now = dt.datetime.now(dt.timezone.utc)
                if await uow.repo.is_user_deleted(username=login):
                    raise AuthBadRequestException(detail=resp_exc.USER_BAD_REQUEST)
                return login, now
            else:
                raise AuthBadRequestException(detail=resp_exc.TOKEN_BAD_REQUEST)

    @staticmethod
    async def get_data_user(
        uow: AuthUOW, token: str, roles: Optional[tuple[str, ...]]
    ) -> UserInfoSchema:
        """Получить данные текущего пользователя."""
        data_user = await CurrentUserDep.get_data_user(roles, token, uow=uow)
        user_info = UserInfoSchema(
            id=data_user["id"],
            email=data_user["email"],
            deleted=data_user["deleted"],
            role_name=data_user["role_name"] if data_user.get("role_name") else None,
        )
        return user_info
