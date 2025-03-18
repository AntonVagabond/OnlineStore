from sqlalchemy import RowMapping

from app.domain.user.entities.user import User
from app.domain.user.value_objects.contacts import Contacts
from app.domain.user.value_objects.username import Username


def result_to_user_entity(user: RowMapping) -> User:
    """Преобразование модели пользователя в сущность User."""
    return User(
        user_id=user["user_id"],
        username=Username(value=user["username"]),
        contacts=Contacts(email=user["email"], phone_number=user["phone_number"]),
    )
