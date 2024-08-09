import base64
from datetime import datetime
from types import NoneType
from typing import Optional, Union, TypeAlias
from uuid import UUID

from common.enums.role import Role
from common.services.base import BaseService

RegisterData: TypeAlias = dict[
    str, Union[bytes, str, datetime, bool, Role, NoneType, int]
]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class ProfileService(BaseService):
    """Сервис для работы с профилем."""
