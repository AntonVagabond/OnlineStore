from common.const import mixins as resp_exc
from common.schemas.responses import mixins as response

LOGIN_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "email_bad_request": {
                        "summary": "Email bad request",
                        "value": {"detail": resp_exc.EMAIL_BAD_REQUEST},
                    },
                    "password_bad_request": {
                        "summary": "Password bad request",
                        "value": {"detail": resp_exc.PASSWORD_BAD_REQUEST},
                    },
                    "user_bad_request": {
                        "summary": "User bad request",
                        "value": {"detail": resp_exc.USER_BAD_REQUEST},
                    },
                }
            }
        },
    },
    401: {"model": response.UnauthorizedResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}

REFRESH_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "user_bad_request": {
                        "summary": "User bad request",
                        "value": {"detail": resp_exc.USER_BAD_REQUEST},
                    },
                    "token_bad_request": {
                        "summary": "Token bad request",
                        "value": {"detail": resp_exc.TOKEN_BAD_REQUEST},
                    },
                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}

AUTH_RESPONSES = {
    400: {"model": response.UserBadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "examples": {
                    "token_expired_forbidden": {
                        "summary": "Token expired forbidden",
                        "value": {"detail": resp_exc.TOKEN_EXPIRED_FORBIDDEN},
                    },
                    "token_invalid_forbidden": {
                        "summary": "Token invalid forbidden",
                        "value": {"detail": resp_exc.TOKEN_INVALID_FORBIDDEN},
                    },
                    "token_required_field_forbidden": {
                        "summary": "Token required field forbidden",
                        "value": {"detail": resp_exc.TOKEN_REQUIRED_FIELD_FORBIDDEN},
                    },
                    "roles_forbidden": {
                        "summary": "Roles forbidden",
                        "value": {"detail": resp_exc.ROLES_FORBIDDEN},
                    },
                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}
