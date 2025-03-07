from dataclasses import asdict

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.common.exception import DomainError
from app.presentation.api.exceptions.base import PresentationError
from app.presentation.api.schemas.base import ErrorData, ErrorResponse


def domain_error_handler(
    request: Request, exception: DomainError, status_code: int  # noqa
) -> JSONResponse:
    """Обработчик доменных исключений."""
    return JSONResponse(
        status_code=status_code,
        content=asdict(
            ErrorResponse(status=status_code, error=ErrorData(data=exception.message))
        ),
    )


def presentation_error_handler(
    request: Request, exception: PresentationError, status_code: int  # noqa
) -> JSONResponse:
    """Обработчик представленных исключений."""
    return JSONResponse(
        status_code=status_code,
        content=asdict(
            ErrorResponse(status=status_code, error=ErrorData(data=exception.message))
        ),
    )


async def internal_exception_handler(
    request: Request, exception: Exception, status_code: int  # noqa
) -> JSONResponse:
    """Обработчик внутренних исключений."""
    return JSONResponse(
        status_code=status_code,
        content=asdict(
            ErrorResponse(
                status=status_code,
                error=ErrorData(data="Internal server error"),
            ),
        ),
    )
