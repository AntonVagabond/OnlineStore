from typing import TYPE_CHECKING, Self

from app.domain.common.aggregate_root import AggregateRoot
from app.domain.user.events.user_created import UserCreated

if TYPE_CHECKING:
    from uuid import UUID

    from app.domain.user.value_objects.contacts import Contacts
    from app.domain.user.value_objects.username import Username


class User(AggregateRoot[UUID]):
    """Класс для определения пользователя."""

    def __init__(self, user_id: UUID, username: Username, contacts: Contacts) -> None:
        super().__init__(entity_id=user_id)
        self.username = username
        self.contacts = contacts

    @classmethod
    def create_user(cls, user_id: UUID, username: Username, contacts: Contacts) -> Self:
        user = cls(user_id=user_id, username=username, contacts=contacts)
        event = UserCreated(
            user_id=user.entity_id,
            username=user.username.value,
            email=user.contacts.email,
            phone_number=user.contacts.phone_number,
        )
        user.record_event(event)
        return user
