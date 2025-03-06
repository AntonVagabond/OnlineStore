from fastapi import FastAPI

from app.presentation.api.routers.user import router as user_router


def setup_routers(app: FastAPI) -> None:
    """Регистрация маршрутов для FastAPI."""
    app.include_router(user_router)
