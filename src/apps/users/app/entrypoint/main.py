from fastapi import FastAPI

from app.entrypoint.di.setup import setup_di
from app.entrypoint.setup import setup_app
from app.presentation.api.setups.exception import setup_exception_handlers
from app.presentation.api.setups.routers import setup_routers


def app_factory() -> FastAPI:
    app = setup_app()
    setup_routers(app)
    setup_di(app)
    setup_exception_handlers(app)
    return app
