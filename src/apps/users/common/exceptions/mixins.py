from fastapi import HTTPException

from common.const import response_exceptions as resp_exc


class UserNotFoundException(HTTPException):
    """Исключение, при отсутствии пользователя в базе данных."""

    def __init__(self) -> None:
        self.status_code = 404
        self.detail = resp_exc.USER_NOT_FOUND
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailAlreadyExistsException(HTTPException):
    """Исключение, при уже существующей электронной почте в базе данных."""

    def __init__(self) -> None:
        self.status_code = 409
        self.detail = resp_exc.EMAIL_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)


class PhoneNumberAlreadyExistsException(HTTPException):
    """Исключение, при уже существующем номере телефона в базе данных."""

    def __init__(self) -> None:
        self.status_code = 409
        self.detail = resp_exc.PHONE_NUMBER_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)
