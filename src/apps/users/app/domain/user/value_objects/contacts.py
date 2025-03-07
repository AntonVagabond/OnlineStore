from dataclasses import dataclass

from ...common.const import exceptions as text
from ...common.value_object import ValueObject
from .. import exceptions as exc


@dataclass(frozen=True)
class Contacts(ValueObject):
    """Объект контактных данных."""

    phone_number: str | None
    email: str | None

    def _validate(self) -> None:
        """Проверка валидности контактных данных."""
        if self.phone_number is None and self.email is None:
            raise exc.EmptyContactError(text.EMPTY_CONTACT)

        if self.phone_number and not isinstance(self.phone_number, str):
            raise exc.WrongPhoneNumberFormatError(text.WRONG_PHONE_NUMBER_FORMAT)

        if self.email and not isinstance(self.email, str):
            raise exc.WrongEmailFormatError(text.WRONG_EMAIL_FORMAT)

    def __str__(self) -> str:
        """Преобразование в строковое представление."""
        if self.phone_number and self.email:
            return f"{self.phone_number} {self.email}"

        if self.phone_number:
            return f"{self.phone_number}"

        return f"{self.email}"
