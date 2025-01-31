from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_cors_middleware(app: FastAPI) -> None:
    """Установка CORS для FastAPI."""
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
