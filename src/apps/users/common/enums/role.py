from enum import IntEnum


class RoleEnum(IntEnum):
    """Роли пользователей."""

    CUSTOMER = 0
    COURIER = 10
    PROVIDER = 20
    MANAGER = 50
    ADMIN = 100
