from abc import ABC
from datetime import datetime
from typing import TypeVar

from sqlalchemy import select, func

from common.models.base import Base
from core.database import async_session_maker
from core.security import hash_password
from models.users import User
from models.roles import Role

TModel = TypeVar("TModel", bound=Base)


class Initializer(ABC):
    """Абстрактный класс инициализации."""
    model = None
    entities = []

    @classmethod
    async def initialize(cls):
        """Инициализация моделей."""
        gener_class_type = cls.model
        async with async_session_maker() as session:
            model_exists = await session.execute(
                select(func.count("*")).select_from(gener_class_type)
            )
            if model_exists.scalar() == 0:
                try:
                    for entity in cls.entities:
                        session.add(gener_class_type(**entity))
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
            else:
                pass


class RoleInitializer(Initializer):
    """Инициализация Роли."""
    model = Role
    entities = [
        {
            "name": 'customer',
            "users": [
                User(
                    username="TestCustomer@gmail.com",
                    last_name="Динаров",
                    first_name="Алмаз",
                    second_name="Антонович",
                    full_name="Динаров Алмаз Антонович",
                    email="TestCustomer@gmail.com",
                    password_hash=hash_password("TestPassword_1111"),
                    phone_number="+7(924)596-30-99",
                    photo=None,
                    birthday=datetime.strptime("1986-2-25", "%Y-%m-%d"),
                    logged_out=False,
                    deleted=False,
                    is_man=True,
                    role_id=None,
                    date_add=datetime.now(),
                    date_update=datetime.now(),
                )
            ],
            "role": 0,
        },
        {
            "name": 'courier',
            "users": [User(
                username="TestCourier@gmail.com",
                last_name="Леонов",
                first_name="Степан",
                second_name="Владимирович",
                full_name="Леонов Степан Владимирович",
                email="TestCourier@gmail.com",
                password_hash=hash_password("TestPassword_2222"),
                phone_number="+7(924)596-30-99",
                photo=None,
                birthday=datetime.strptime("1986-2-25", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                date_add=datetime.now(),
                date_update=datetime.now(),
            )],
            "role": 10,
        },
        {
            "name": 'provider',
            "users": [User(
                username="TestProvider@gmail.com",
                last_name="Матвеева",
                first_name="Диляра",
                second_name="Анатольевна",
                full_name="Матвеева Диляра Анатольевна",
                email="TestProvider@gmail.com",
                password_hash=hash_password("TestPassword_3333"),
                phone_number="+7(922)523-11-22",
                photo=None,
                birthday=datetime.strptime("1999-12-19", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                date_add=datetime.now(),
                date_update=datetime.now(),
            )],
            "role": 20,
        },
        {
            "name": 'manager',
            "users": [User(
                username="TestManager@gmail.com",
                last_name="Горбачев",
                first_name="Динар",
                second_name="Олегович",
                full_name="Горбачев Динар Олегович",
                email="TestManager@gmail.com",
                password_hash=hash_password("TestPassword_4444"),
                phone_number="+7(954)511-99-22",
                photo=None,
                birthday=datetime.strptime("1974-06-03", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                date_add=datetime.now(),
                date_update=datetime.now(),
            )],
            "role": 50,
        },
        {
            "name": 'admin',
            "users": [User(
                username="TestAdmin@gmail.com",
                last_name="Долотов",
                first_name="Давид",
                second_name="Альмирович",
                full_name="Долотов Давид Альмирович",
                email="TestAdmin@gmail.com",
                password_hash=hash_password("TestPassword_5555"),
                phone_number="+7(954)511-99-22",
                photo=None,
                birthday=datetime.strptime("1974-06-03", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                date_add=datetime.now(),
                date_update=datetime.now(),
            )],
            "role": 100,
        },
    ]
