from dataclasses import dataclass

from ...common.value_object import ValueObject
from ..exceptions.value_objects import InvalidContactsError


@dataclass(frozen=True)
class Contacts(ValueObject):
    """Объект контактных данных."""

    phone_number: str | None
    email: str | None

    def _validate(self) -> None:
        """Проверка валидности контактных данных."""
        if self.phone_number is None and self.email is None:
            raise InvalidContactsError(
                "Необходимо указать хотя бы один контактный номер."
            )

        if self.phone_number and not isinstance(self.phone_number, str):
            raise InvalidContactsError(
                "Телефонный номер должен быть указан в строковом значении."
            )

        if self.email and not isinstance(self.email, str):
            raise InvalidContactsError("Почта должна быть указана в строковом значении.")

    def __str__(self) -> str:
        """Преобразование в строковое представление."""
        if self.phone_number and self.email:
            return f"{self.phone_number} {self.email}"

        if self.phone_number:
            return f"{self.phone_number}"

        return f"{self.email}"
