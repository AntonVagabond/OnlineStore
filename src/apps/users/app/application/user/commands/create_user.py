from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.common.const import exceptions as text
from app.domain.user.entities.user import User
from app.domain.user.exceptions import entity as exc

from ...common.handler import Handler

if TYPE_CHECKING:
    from app.application.common.unit_of_work import IUnitOfWork
    from app.domain.user.repositories.user_repository import IUserRepository

    from ...common.event_bus import IEventBus


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    email: str | None
    phone_number: str | None


class CreateUserHandler(Handler[CreateUserCommand, UUID]):
    """Класс-обработчик для создания пользователя."""

    def __init__(
        self, uow: IUnitOfWork, user_repository: IUserRepository, event_bus: IEventBus
    ) -> None:
        self.__uow = uow
        self.__user_repository = user_repository
        self.__event_bus = event_bus

    async def handle(self, command: CreateUserCommand) -> UUID:
        """Создание пользователя."""
        if command.email and await self.__user_repository.is_exists_email(command.email):
            raise exc.EmailAlreadyExistsError(text.EMAIL_CONFLICT)

        if command.phone_number and await self.__user_repository.is_exists_phone_number(
            command.phone_number
        ):
            raise exc.PhoneNumberAlreadyExistsError(text.PHONE_NUMBER_CONFLICT)

        if await self.__user_repository.is_exists_username(command.username):
            raise exc.UserAlreadyExistsError(text.USER_CONFLICT)

        user_uuid = uuid4()

        user = User.create_user(
            user_id=user_uuid,
            username=command.username,
            phone_number=command.phone_number,
            email=command.email,
        )
        events = user.raise_events()

        self.__user_repository.add(user)
        await self.__event_bus.publish(events=events)
        await self.__uow.commit()

        return user_uuid
