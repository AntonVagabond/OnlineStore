from functools import partial

from fastapi import FastAPI
from starlette import status

from app.application.user import exceptions as application_user_exc
from app.domain.user import exceptions as domain_user_exc
from app.presentation.api.exceptions import exceptions as presentation_exc
from app.presentation.api.exceptions.handlers import (
    domain_error_handler,
    internal_exception_handler,
    presentation_error_handler,
)


def setup_exception_handlers(app: FastAPI) -> None:
    """Регистрация обработчиков исключений для FastAPI."""
    app.add_exception_handler(
        domain_user_exc.EmptyUsernameError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        domain_user_exc.WrongUsernameFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        domain_user_exc.EmptyContactError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        domain_user_exc.WrongPhoneNumberFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        domain_user_exc.WrongEmailFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )

    app.add_exception_handler(
        presentation_exc.UnauthorizedError,
        partial(presentation_error_handler, status_code=status.HTTP_401_UNAUTHORIZED),
    )

    app.add_exception_handler(
        application_user_exc.UserAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        application_user_exc.EmailAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        application_user_exc.PhoneNumberAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )

    app.add_exception_handler(
        Exception,
        partial(
            internal_exception_handler, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
    )
