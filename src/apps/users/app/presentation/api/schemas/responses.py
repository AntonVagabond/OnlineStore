from dataclasses import dataclass, field
from typing import Generic, TypeVar

ResultT = TypeVar("ResultT")
ErrorT = TypeVar("ErrorT")


@dataclass(frozen=True)
class Response:
    """Класс ответа на результат запроса."""

    status: int


@dataclass(frozen=True)
class SuccessfulResponse(Response, Generic[ResultT]):
    """Класс реализующий успешный ответ на запрос."""

    result: ResultT | None = field(default=None)


@dataclass(frozen=True)
class ErrorData(Generic[ErrorT]):
    """Класс с данными ошибки."""

    title: str = "Произошла ошибка"
    data: ErrorT | None = field(default=None)


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[ErrorT]):
    """Класс реализующий ответ ошибку на запрос."""

    error: ErrorData[ErrorT] = field(default_factory=ErrorData)
