import abc
from typing import Type, TypeVar, Generic

from common.repositories.base import BaseRepository

TRepository = TypeVar("TRepository", bound=BaseRepository)


class IUnitOfWork(abc.ABC, Generic[TRepository]):
    """Абстрактный класс для работы с транзакциями."""
    repo: Type[TRepository]

    @abc.abstractmethod
    def __init__(self) -> None:
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> TRepository:
        """Абстрактный метод входа в контекстного менеджера."""

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None:
        """Абстрактный метод выхода из контекстного менеджера"""

    @abc.abstractmethod
    async def commit(self) -> None:
        """Абстрактный метод фиксирования транзакции."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Абстрактный метод завершения транзакции."""
