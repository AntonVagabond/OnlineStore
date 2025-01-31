from typing import TYPE_CHECKING

from app.presentation.api.controllers.user import router as user_router
from app.presentation.api.middlewares.cors_middleware import setup_cors_middleware

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_middlewares(app: FastAPI) -> None:
    """Установка мидлвейр для FastAPI."""
    setup_cors_middleware(app)


def setup_routes(app: FastAPI) -> None:
    """Регистрация маршрутов для FastAPI."""
    app.include_router(user_router)
