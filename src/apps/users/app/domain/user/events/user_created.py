from dataclasses import dataclass
from uuid import UUID

from ...common.event import Event


@dataclass(frozen=True)
class UserCreated(Event["UserCreated"]):
    """Событие создания пользователя."""

    user_id: UUID
    username: str
    email: str | None
    phone_number: str | None
