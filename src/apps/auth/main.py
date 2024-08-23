from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from api.v1.routers import all_routers_v1
from core.config import settings
from core.logger import LoggerConfig


# region ------------------------------ initialize ----------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa
    yield


# endregion -------------------------------------------------------------------------


# region ---------------------------- APPLICATION -----------------------------------
app = FastAPI(
    lifespan=lifespan,
    openapi_url=settings.openapi_url,
    swagger_ui_init_oauth={
        "clientId": settings.client_id,
        "clientSecret": settings.client_secret,
    }
)


# endregion -------------------------------------------------------------------------


# region -------------------------------- SWAGGER -----------------------------------
def custom_openapi():
    """Swagger configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Auth",
        version="1.0",
        summary="Микросервис для авторизации и аутентификации пользователя.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
# endregion -------------------------------------------------------------------------


# region -------------------------------- CORS --------------------------------------
# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)
# endregion -------------------------------------------------------------------------

# region -------------------------------- Routing -----------------------------------
for router in all_routers_v1:
    app.include_router(router)
# endregion -------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_config=LoggerConfig.execute_config()
    )
