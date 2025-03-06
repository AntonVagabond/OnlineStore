from fastapi import FastAPI

from app.presentation.api.middlewares.cors_middleware import setup_cors_middleware


def setup_middlewares(app: FastAPI) -> None:
    """Установка промежуточного слоя для FastAPI."""
    setup_cors_middleware(app)
