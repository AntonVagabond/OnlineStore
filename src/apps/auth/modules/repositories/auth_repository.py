from datetime import datetime
from typing import Generator, Optional

from typing_extensions import Union

from common.repositories.base import BaseRepository


class AuthRepository(BaseRepository):
    """Репозиторий аутентификации."""

    async def get_user_for_authorization(self, username: str) -> Optional[list[str]]:
        """Получение пользователя для авторизации."""
        key = f"user:{username}"
        results = await self.session.hmget(
            name=key, keys=["login", "hash_password", "deleted", "expire_devices"]
        )
        return None if all(field is None for field in results) else results

    async def set_user(self, data: dict[str, str]) -> None:
        """Сохранение пользователя."""
        key = f"user:{data['login']}"
        await self.session.hset(name=key, mapping=data)

    @staticmethod
    def __gen_filter_devices(
        current_expire_device: datetime, expire_devices: str
    ) -> Generator[str, None, None]:
        """Генератор фильтрации истекшего времени у устройств."""
        for expire_device in expire_devices.split(","):
            datetime_expire = datetime.strptime(expire_device, "%Y-%m-%d %H:%M:%S")
            if datetime_expire != current_expire_device.replace(tzinfo=None):
                yield expire_device

    async def delete_expire_device(self, username: str, exp_device: datetime) -> None:
        """
        Удаление истекшего времени устройства/устройств
        из списка времён подключенных устройств.
        """
        key = f"user:{username}"
        expire_devices = await self.session.hget(name=key, key="expire_devices")

        filter_expire_devices = ",".join(
            self.__gen_filter_devices(exp_device, expire_devices)
        )
        if not filter_expire_devices:
            await self.session.delete(key)
        else:
            await self.session.hset(
                name=key, key="expire_devices", value=filter_expire_devices
            )

    async def is_user_deleted(self, username: str) -> bool:
        """Проверка удалённости пользователя."""
        key = f"user:{username}"
        result = await self.session.hget(name=key, key="deleted")
        return False if result == "0" else True

    async def get_user_for_authentication(
        self, username: str
    ) -> Optional[dict[str, Union[str, bytes]]]:
        """Получение пользователя для аутентификации."""
        key = f"user:{username}"
        results = await self.session.hgetall(name=key)
        return results if results else None
