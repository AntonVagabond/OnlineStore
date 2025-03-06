from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_cors_middleware(app: FastAPI) -> None:
    """Установка CORS для FastAPI."""
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET", "DELETE", "PUT"],
        allow_headers=["*"],
    )
