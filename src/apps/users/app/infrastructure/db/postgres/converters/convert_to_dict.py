from typing import TYPE_CHECKING

from app.domain.user.entities.user import User

if TYPE_CHECKING:
    from uuid import UUID


def user_entity_to_dict(user: User) -> dict[str, UUID | str]:
    """Преобразовать сущность пользователя в словарь."""
    return {
        "user_id": user.entity_id,
        "email": user.contacts.email,
        "phone_number": user.contacts.phone_number,
        "username": user.username.value,
    }
