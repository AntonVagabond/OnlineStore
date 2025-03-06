from dataclasses import asdict

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.common.exception import DomainError
from app.presentation.api.exceptions.base import PresentationError
from app.presentation.api.schemas.base import ErrorData, ErrorResponse


def domain_error_handler(
    request: Request, exception: DomainError, status: int  # noqa
) -> JSONResponse:
    """Обработчик доменных исключений."""
    return JSONResponse(
        status_code=status,
        content=asdict(
            ErrorResponse(status=status, error=ErrorData(data=exception.message))
        ),
    )


def presentation_error_handler(
    request: Request, exception: PresentationError, status: int  # noqa
) -> JSONResponse:
    """Обработчик представленных исключений."""
    return JSONResponse(
        status_code=status,
        content=asdict(
            ErrorResponse(status=status, error=ErrorData(data=exception.message))
        ),
    )


async def internal_exception_handler(
    request: Request, exception: Exception, status: int  # noqa
) -> JSONResponse:
    """Обработчик внутренних исключений."""
    return JSONResponse(
        status_code=status,
        content=asdict(
            ErrorResponse(
                status=status,
                error=ErrorData(data="Internal server error"),
            ),
        ),
    )
