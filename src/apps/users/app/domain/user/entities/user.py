from typing import Self
from uuid import UUID

from ...common.aggregate_root import AggregateRoot
from ..events.user_created import UserCreated
from ..value_objects.contacts import Contacts
from ..value_objects.username import Username


class User(AggregateRoot[UUID]):
    """Класс для определения пользователя."""

    __slots__ = ("username", "contacts")

    def __init__(self, user_id: UUID, username: Username, contacts: Contacts) -> None:
        super().__init__(entity_id=user_id)
        self.username = username
        self.contacts = contacts

    @classmethod
    def create_user(
        cls, user_id: UUID, username: str, phone_number: str, email: str
    ) -> Self:
        """Создание нового пользователя."""
        username = Username(value=username)
        contacts = Contacts(phone_number=phone_number, email=email)

        user = cls(user_id=user_id, username=username, contacts=contacts)
        event = UserCreated(
            user_id=user.entity_id,
            username=user.username.value,
            email=user.contacts.email,
            phone_number=user.contacts.phone_number,
        )
        user.record_event(event)
        return user
