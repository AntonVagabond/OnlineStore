from uuid import UUID

from starlette import status

from app.application.common.dto.user_dto import UserDto
from app.application.user import exceptions as application_user_exc
from app.domain.user import exceptions as domain_user_exc

from ...exceptions.exceptions import UnauthorizedError
from ..base import ErrorResponse, SuccessfulResponse

CREATE_USER_RESPONSES = {
    status.HTTP_201_CREATED: {
        "model": SuccessfulResponse[UUID],
    },
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse[
            domain_user_exc.TooLongUsernameError
            | domain_user_exc.EmptyUsernameError
            | domain_user_exc.WrongUsernameFormatError
            | domain_user_exc.EmptyContactError
            | domain_user_exc.WrongPhoneNumberFormatError
            | domain_user_exc.WrongEmailFormatError
        ],
    },
    status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[UnauthorizedError]},
    status.HTTP_409_CONFLICT: {
        "model": ErrorResponse[
            application_user_exc.UserAlreadyExistsError
            | application_user_exc.EmailAlreadyExistsError
            | application_user_exc.PhoneNumberAlreadyExistsError
        ],
    },
}

GET_USER_RESPONSES = {
    status.HTTP_200_OK: {
        "model": SuccessfulResponse[UserDto],
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse[application_user_exc.UserNotFoundError]
    },
}
