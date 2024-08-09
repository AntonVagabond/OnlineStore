from __future__ import annotations

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.profiles import ProfileRepository


class ProfileUOW(BaseUnitOfWork[ProfileRepository]):
    """Класс для работы с транзакциями профиля."""
