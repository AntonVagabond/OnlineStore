from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from ..config import AppConfig


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """Swagger configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User",
        version="1.0",
        summary="Микросервис для работы с пользователем.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_app(lifespan: asynccontextmanager, config: AppConfig) -> FastAPI:
    """Настройка приложения."""
    app = FastAPI(
        lifespan=lifespan,
        openapi_url=config.openapi_url,
        swagger_ui_init_oauth={
            "clientId": config.client_id,
            "clientSecret": config.client_secret,
        },
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )
    app.openapi = lambda: custom_openapi(app)
    return app
