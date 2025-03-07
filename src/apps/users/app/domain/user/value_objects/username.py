import re
from dataclasses import dataclass

from ...common.const import exceptions as text
from ...common.value_object import ValueObject
from .. import exceptions as exc


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
            raise exc.EmptyUsernameError(text.EMPTY_USERNAME)
        if len(self.value) > self.__MAX_LENGTH:
            raise exc.TooLongUsernameError(text.TOO_LONG_USERNAME(self.__MAX_LENGTH))
        if not self.__PATTERN.match(self.value):
            raise exc.WrongUsernameFormatError(text.WRONG_USERNAME_FORMAT)
