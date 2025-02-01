from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.user.entities.user import User
from app.domain.user.exceptions.entity import UserAlreadyExistsError
from app.domain.user.value_objects.contacts import Contacts
from app.domain.user.value_objects.username import Username

if TYPE_CHECKING:
    from app.application.common.event_bus import EventBus
    from app.domain.user.repositories.user_repository import UserRepository
    from app.infrastructure.common.protocols.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    email: str | None
    phone_number: str | None


class CreateUserHandler:
    """Класс-обработчик для создания пользователя."""

    def __init__(
        self, uow: UnitOfWork, user_repository: UserRepository, event_bus: EventBus
    ) -> None:
        self.uow = uow
        self.user_repository = user_repository
        self.event_bus = event_bus

    async def handle(self, command: CreateUserCommand) -> UUID:
        """Создание пользователя."""
        if command.email and await self.user_repository.is_exists_email(command.email):
            raise UserAlreadyExistsError("Пользователь не найден.")

        if command.phone_number and await self.user_repository.is_exists_phone_number(
            command.phone_number
        ):
            raise UserAlreadyExistsError("Пользователь не найден.")

        if await self.user_repository.is_exists_username(command.username):
            raise UserAlreadyExistsError("Пользователь не найден.")

        user_uuid = uuid4()
        username = Username(value=command.username)
        contacts = Contacts(phone_number=command.phone_number, email=command.email)

        user = User.create_user(user_id=user_uuid, username=username, contacts=contacts)

        self.uow.register_new(user)
        await self.event_bus.publish(user.raise_events())
        await self.uow.commit()

        return user_uuid
