from functools import partial

from fastapi import FastAPI
from starlette import status

from app.domain.user.exceptions import entity, value_objects
from app.presentation.api.exceptions import authorized
from app.presentation.api.exceptions.handlers import (
    domain_error_handler,
    internal_exception_handler,
    presentation_error_handler,
)


def setup_exception_handlers(app: FastAPI) -> None:
    """Регистрация обработчиков исключений для FastAPI."""
    app.add_exception_handler(
        value_objects.EmptyUsernameError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        value_objects.EmptyUsernameError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        value_objects.WrongUsernameFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        value_objects.EmptyContactError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        value_objects.WrongPhoneNumberFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        value_objects.WrongEmailFormatError,
        partial(domain_error_handler, status_code=status.HTTP_400_BAD_REQUEST),
    )

    app.add_exception_handler(
        authorized.UnauthorizedError,
        partial(presentation_error_handler, status_code=status.HTTP_401_UNAUTHORIZED),
    )

    app.add_exception_handler(
        entity.UserAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        entity.EmailAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        entity.PhoneNumberAlreadyExistsError,
        partial(domain_error_handler, status_code=status.HTTP_409_CONFLICT),
    )

    app.add_exception_handler(
        Exception,
        partial(
            internal_exception_handler, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
    )
