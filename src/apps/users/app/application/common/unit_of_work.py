import abc
from typing import Protocol

from app.domain.common.entity import Entity


class UnitOfWork(Protocol):
    """Протокол для управления транзакциями."""

    @abc.abstractmethod
    def register_new(self, entity: Entity) -> None:
        """Регистрация новой сущности."""
        raise NotImplementedError

    @abc.abstractmethod
    def register_dirty(self, entity: Entity) -> None:
        """Регистрация изменения существующей сущности."""
        raise NotImplementedError

    @abc.abstractmethod
    def register_deleted(self, entity: Entity) -> None:
        """Регистрация удаления существующей сущности."""
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self) -> None:
        """Метод фиксирования транзакции."""
        raise NotImplementedError
