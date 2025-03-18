from app.application.common.dto.user_dto import UserDto


def result_to_user_dto(user: ...) -> UserDto:
    return UserDto(
        user_id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
    )
