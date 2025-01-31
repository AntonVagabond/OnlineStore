from typing import Protocol

from app.application.common.transaction import UnitOfWorkTransaction
from app.domain.common.tracker import UnitOfWorkTracker


class UnitOfWork(Protocol, UnitOfWorkTransaction, UnitOfWorkTracker):
    """
    Класс объединяющий в себе работу с транзакциями и отслеживание изменения сущностей.
    """
