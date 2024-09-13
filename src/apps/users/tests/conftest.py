import asyncio
from typing import Generator, AsyncGenerator, Any

import psycopg2
import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pytest_alembic import Config, runner
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import close_all_sessions, Session, sessionmaker

from core.config import settings
from core.database import async_session_maker, sync_session_maker
from main import app
from modules.unit_of_works.admin_panels import AdminPanelUOW
from modules.unit_of_works.profiles import ProfileUOW
from tests.unit.fixtures.admin_panels import AdminTestUOW
from tests.unit.fixtures.profiles import ProfileTestUOW
from utils.initializer import RoleInitializer

pytest_plugins = (
    "tests.unit.fixtures.admin_panels",
    "tests.unit.fixtures.profiles",
)


@pytest.fixture(scope="session")
def monkeypatch_session() -> Generator[MonkeyPatch, None, None]:
    """Имитирование объекта MonkeyPatch для тестовых сессий."""
    monkeypatch = MonkeyPatch()
    try:
        yield monkeypatch
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Создание отдельного цикла событий для тестовой сессии."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# region -------------------------------- DATABASE ---------------------------------------
@pytest.fixture(scope="session", autouse=True)
def __mock_db_url(monkeypatch_session: MonkeyPatch) -> None:
    """Имитирование URL базы данных для тестовых сессий."""
    async_database_url: URL = settings.db.async_database_url
    sync_database_url: URL = settings.db.sync_database_url
    monkeypatch_session.setattr(
        target=settings.db,
        name="async_database_url",
        value=async_database_url.set(database="test"),
    )
    monkeypatch_session.setattr(
        target=settings.db,
        name="sync_database_url",
        value=sync_database_url.set(database="test"),
    )
    monkeypatch_session.setenv(name="pg_database", value="test")
    monkeypatch_session.setattr(target=settings.db, name="pg_database", value="test")


@pytest.fixture(scope="session", autouse=True)
def __create_database(__mock_db_url: None) -> Generator[None, None, None]:
    """Создание тестовой базы данных."""
    con = psycopg2.connect(
        f"postgresql://{settings.db.pg_user}:{settings.db.pg_password}@"
        f"{settings.db.pg_host}:{settings.db.pg_port}",
    )

    # Этот параметр позволит выполнять команды SQL вне транзакции, что нужно для
    # таких команд, как CREATE DATABASE и DROP DATABASE, которые нельзя выполнять
    # внутри транзакции.
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = con.cursor()
    cursor.execute(f"""DROP DATABASE IF EXISTS {settings.db.pg_database};""")
    cursor.execute(f"""CREATE DATABASE {settings.db.pg_database};""")
    yield
    close_all_sessions()
    cursor.execute(f"""DROP DATABASE IF EXISTS {settings.db.pg_database};""")


@pytest.fixture(scope="session", autouse=True)
def __mock_sessions_factories(
    async_db_engine: AsyncEngine,
    sync_db_engine: Engine,
) -> None:
    """
    Имитирует 'engine_async' и 'engine_sync' из 'core.database'.
    Это должно предотвратить ошибки в промежуточных программах, использующих эти методы.
    """
    async_session_maker.configure(bind=async_db_engine)
    sync_session_maker.configure(bind=sync_db_engine)


@pytest.fixture(scope="session")
def sync_db_engine() -> Generator[Engine, None, None]:
    """Создание синхронного движка для тестовой базы данных."""
    sync_engine = create_engine(settings.db.sync_database_url)
    try:
        yield sync_engine
    finally:
        close_all_sessions()
        sync_engine.dispose()


@pytest.fixture(scope="session")
async def async_db_engine(
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[AsyncEngine, None]:
    """Создание асинхронного движка для тестовой базы данных."""
    async_engine = create_async_engine(settings.db.async_database_url)
    try:
        yield async_engine
    finally:
        close_all_sessions()
        await async_engine.dispose()


@pytest.fixture(scope="function")
async def sync_session_factory(sync_db_engine: Engine) -> sessionmaker[Session]:
    """Создание синхронной фабрики сессий."""
    return sessionmaker(sync_db_engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def async_session_factory(
    async_db_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Создание асинхронной фабрики сессий."""
    return async_sessionmaker(async_db_engine, expire_on_commit=False)


# endregion ------------------------------------------------------------------------------


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    """Инициализация класса Config библиотеки 'pytest_alembic'."""
    return Config()


@pytest.fixture(scope="session")
def alembic_engine(sync_db_engine: Engine) -> Engine:
    """
    Прокси-сервер 'sync_db_engine' подключается к pytest_alembic
    (сделан движком по умолчанию).
    """
    return sync_db_engine


@pytest.fixture(scope="session")
def alembic_runner(
    alembic_config: Config, alembic_engine: Engine
) -> Generator[runner, None, None]:
    """Запуск программы для настройки pytest_alembic."""
    config = Config.from_raw_config(raw_config=alembic_config)
    with runner(config=config, engine=alembic_engine) as alembic_runner:
        yield alembic_runner


@pytest.fixture(scope="session", autouse=True)
def __apply_migrations(
    __create_database: None,
    alembic_runner: runner,
    alembic_engine: Engine,
) -> Generator[None, None, None]:
    """Применяет все миграции от базовой до последней (через pytest_alembic)."""
    alembic_runner.migrate_up_to(revision="head")
    yield
    alembic_runner.migrate_down_to(revision="base")


@pytest.fixture(scope="session", autouse=True)
async def __initialize_table(
    __apply_migrations: None,
    __mock_sessions_factories: None,
    *,
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[None, None]:
    """Инициализация тестовой таблицы."""
    await RoleInitializer.initialize()
    yield


@pytest.fixture(scope="function")
async def app_fixture(
    sync_session_factory: sessionmaker[Session],
    async_session_factory: async_sessionmaker[AsyncSession],
    monkeypatch: MonkeyPatch,
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[FastAPI, None]:
    """Создание экземпляра FastAPI в тестовом окружении."""

    def generator_dependency_override() -> Generator[tuple[Any, Any], None, None]:
        """Объект для переопределения зависимостей."""
        dict_dep_overrides = {
            sync_session_maker: sync_session_factory,
            async_session_maker: async_session_factory,
            AdminPanelUOW: AdminTestUOW,
            ProfileUOW: ProfileTestUOW,
        }
        yield from dict_dep_overrides.items()

    for key, value in generator_dependency_override():
        app.dependency_overrides[key] = value

    yield app
    app.dependency_overrides = {}
