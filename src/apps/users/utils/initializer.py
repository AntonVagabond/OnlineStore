from abc import ABC
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, func

from core.database import async_session_maker
from core.security import hash_password
from models.roles import Role
from models.users import User


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
                    id=UUID("beb247ae-58cc-4e75-b6fc-61e57e10a606"),
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
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            ],
            "role": 0,
        },
        {
            "name": 'courier',
            "users": [User(
                id=UUID("922f323e-abda-4192-b9f8-c9091fd2686d"),
                username="TestCourier@gmail.com",
                last_name="Леонов",
                first_name="Степан",
                second_name="Владимирович",
                full_name="Леонов Степан Владимирович",
                email="TestCourier@gmail.com",
                password_hash=hash_password("TestPassword_2222"),
                phone_number="+7(924)596-30-92",
                photo=None,
                birthday=datetime.strptime("1986-2-25", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )],
            "role": 10,
        },
        {
            "name": 'provider',
            "users": [User(
                id=UUID("1c44d798-a6a4-4baa-abc6-b243599a1472"),
                username="TestProvider@gmail.com",
                last_name="Матвеева",
                first_name="Диляра",
                second_name="Анатольевна",
                full_name="Матвеева Диляра Анатольевна",
                email="TestProvider@gmail.com",
                password_hash=hash_password("TestPassword_3333"),
                phone_number="+7(922)523-11-23",
                photo=None,
                birthday=datetime.strptime("1999-12-19", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )],
            "role": 20,
        },
        {
            "name": 'manager',
            "users": [User(
                id=UUID("348bf57f-06a1-44f4-b025-c6c4fad5be09"),
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
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )],
            "role": 50,
        },
        {
            "name": 'admin',
            "users": [User(
                id=UUID("8f3fd250-c810-4395-83bb-782ef8a1b79e"),
                username="TestAdmin@gmail.com",
                last_name="Долотов",
                first_name="Давид",
                second_name="Альмирович",
                full_name="Долотов Давид Альмирович",
                email="TestAdmin@gmail.com",
                password_hash=hash_password("TestPassword_5555"),
                phone_number="+7(954)511-99-11",
                photo=None,
                birthday=datetime.strptime("1974-06-03", "%Y-%m-%d"),
                logged_out=False,
                deleted=False,
                is_man=True,
                role_id=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )],
            "role": 100,
        },
    ]
