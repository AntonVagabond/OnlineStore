from typing import Annotated

from pydantic import AfterValidator


class ExtendedTypes:
    """Расширенные типы."""

    @staticmethod
    def validate_int16(value: int) -> int:
        """Валидация числового значения, чтобы оно было как тип int16."""
        if value > 32767 or value <= 0:
            raise ValueError("Значение должно быть типа int16, а не 0!")
        return value

    @staticmethod
    def validate_int64(value: int) -> int:
        """Валидация числового значения, чтобы оно было как тип int64."""
        if value > 9223372036854775807 or value <= 0:
            raise ValueError("Значение должно быть типа int64, а не 0!")
        return value

    Int16 = Annotated[int, AfterValidator(validate_int16)]
    Int64 = Annotated[int, AfterValidator(validate_int64)]
