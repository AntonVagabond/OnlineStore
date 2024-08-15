from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Исключение, при отсутствии пользователя в базе данных."""
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "Пользователь не найден."
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailAlreadyExistsException(HTTPException):
    """Исключение, при уже существующей электронной почте в базе данных."""
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "Такая почта уже существует."
        super().__init__(status_code=self.status_code, detail=self.detail)


class PhoneNumberAlreadyExistsException(HTTPException):
    """Исключение, при уже существующем номере телефона в базе данных."""
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "Такой номер телефона уже существует."
        super().__init__(status_code=self.status_code, detail=self.detail)
