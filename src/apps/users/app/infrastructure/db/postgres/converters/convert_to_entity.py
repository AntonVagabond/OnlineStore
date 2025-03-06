from typing import TYPE_CHECKING

from app.domain.user.entities.user import User
from app.domain.user.value_objects.contacts import Contacts
from app.domain.user.value_objects.username import Username

if TYPE_CHECKING:
    from app.infrastructure.db.postgres.models.user import UserTable


def result_to_user_entity(user: UserTable) -> User:
    """Преобразование модели пользователя в сущность User."""
    return User(
        user_id=user.id,
        username=Username(value=user.username),
        contacts=Contacts(email=user.email, phone_number=user.phone_number),
    )
