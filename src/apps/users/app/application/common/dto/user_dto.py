from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserDto:
    user_id: UUID
    username: str
    email: str | None
    phone_number: int | None
