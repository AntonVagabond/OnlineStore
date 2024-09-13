from fastapi import HTTPException


class AuthUnauthorizedException(HTTPException):
    """Исключение, при неправильном или истекшем токене аутентификации."""

    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "Не удалось подтвердить учетные данные"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class AuthForbiddenException(HTTPException):
    """Исключение, при запрещенном доступе."""

    def __init__(self, detail: str) -> None:
        self.status_code = 403
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class AuthBadRequestException(HTTPException):
    """Исключение, при неправильном запросе."""

    def __init__(self, detail: str) -> None:
        self.status_code = 400
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )
