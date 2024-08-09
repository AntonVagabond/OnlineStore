from enum import IntEnum


class Role(IntEnum):
    """Роли пользователей."""
    CUSTOMER = 0
    COURIER = 10
    PROVIDER = 20
    MANAGER = 50
    ADMIN = 100
