from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from common.schemas.base import BaseModel


class ProfileResponseSchema(BaseModel):
    """Схема ответа на запрос профиля."""
    id: str
    last_name: str
    first_name: str
    second_name: str
    phone_number: str
    email: EmailStr
    is_man: bool
    photo: Optional[...]
    birthday: datetime
    date_added: str
