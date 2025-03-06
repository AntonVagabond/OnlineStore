from uuid import UUID

from starlette import status

from app.domain.user.exceptions import entity, value_objects

from ...exceptions.authorized import UnauthorizedError
from ..base import ErrorResponse, SuccessfulResponse

CREATE_USER_RESPONSES = {
    status.HTTP_201_CREATED: {
        "model": SuccessfulResponse[UUID],
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse[
            value_objects.TooLongUsernameError
            | value_objects.EmptyUsernameError
            | value_objects.WrongUsernameFormatError
            | value_objects.EmptyContactError
            | value_objects.WrongPhoneNumberFormatError
            | value_objects.WrongEmailFormatError
        ],
    },
    status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[UnauthorizedError]},
    status.HTTP_409_CONFLICT: {
        "model": ErrorResponse[
            entity.UserAlreadyExistsError
            | entity.EmailAlreadyExistsError
            | entity.PhoneNumberAlreadyExistsError
        ],
    },
}
