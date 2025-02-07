import re
from dataclasses import dataclass

from ...common.value_object import ValueObject
from ..exceptions.value_objects import InvalidUsernameError


@dataclass(frozen=True)
class Username(ValueObject):
    """Объект никнейм пользователя."""

    __MAX_LENGTH = 32
    __PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")

    value: str | None

    def _validate(self) -> None:
        """Проверка валидности никнейма пользователя."""
        if self.value is None:
            return
        if len(self.value) == 0:
            raise InvalidUsernameError("Никнейм пользователя не может быть пустым.")
        if len(self.value) > self.__MAX_LENGTH:
            raise InvalidUsernameError(
                "Никнейм пользователя не может быть длиннее "
                f"{self.__MAX_LENGTH} символов."
            )
        if not self.__PATTERN.match(self.value):
            raise InvalidUsernameError(
                "Никнейм пользователя должен начинаться с буквы и содержать "
                "только латинские буквы, цифры, и знак подчеркивания."
            )
