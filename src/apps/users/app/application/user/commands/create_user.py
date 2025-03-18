from dataclasses import dataclass
from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.common.id_generator import IdGenerator
from app.domain.user.entities.user import User
from app.domain.user.repositories.user_repository import UserRepository

from ...common.const import exceptions as text
from ...common.event_bus import EventBus
from ...common.handler import CommandHandler
from .. import exceptions as exc


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    email: str | None
    phone_number: str | None


class CreateUserHandler(CommandHandler[CreateUserCommand, UUID]):
    """Класс-обработчик для создания пользователя."""

    __slots__ = ("unit_of_work", "id_generator", "user_repository", "event_bus")

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        id_generator: IdGenerator,
        user_repository: UserRepository,
        event_bus: EventBus,
    ) -> None:
        self.unit_of_work = unit_of_work
        self.id_generator = id_generator
        self.user_repository = user_repository
        self.event_bus = event_bus

    async def handle(self, command: CreateUserCommand) -> UUID:
        """Создание пользователя."""
        if command.email and await self.user_repository.is_exists_email(command.email):
            raise exc.EmailAlreadyExistsError(text.EMAIL_CONFLICT)

        if command.phone_number and await self.user_repository.is_exists_phone_number(
            command.phone_number
        ):
            raise exc.PhoneNumberAlreadyExistsError(text.PHONE_NUMBER_CONFLICT)

        if await self.user_repository.is_exists_username(command.username):
            raise exc.UserAlreadyExistsError(text.USER_CONFLICT)

        user_uuid = self.id_generator.generate()

        user = User.create_user(
            user_id=user_uuid,
            username=command.username,
            phone_number=command.phone_number,
            email=command.email,
        )
        events = user.raise_events()

        self.user_repository.add(user)
        await self.event_bus.publish(events=events)
        await self.unit_of_work.commit()

        return user_uuid
