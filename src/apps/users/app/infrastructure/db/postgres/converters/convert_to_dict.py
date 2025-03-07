from uuid import UUID

from app.domain.user.entities.user import User


def user_entity_to_dict(user: User) -> dict[str, UUID | str]:
    """Преобразовать сущность пользователя в словарь."""
    return {
        "user_id": user.entity_id,
        "email": user.contacts.email,
        "phone_number": user.contacts.phone_number,
        "username": user.username.value,
    }
