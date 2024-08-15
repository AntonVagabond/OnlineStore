from common.schemas.responses import mixins as response
from modules.schemas.profiles import ProfileResponseSchema

REGISTRATION_RESPONSES = {
        200: {"model": response.SuccessIdResponseSchema},
        400: {"model": response.BadRequestResponseSchema},
        401: {"model": response.UnauthorizedResponseSchema},
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "examples": {
                        "email_conflict": {
                            "summary": "Email already exists",
                            "value": {"detail": "Такая почта уже существует."},
                        },
                        "phone_number_conflict": {
                            "summary": "Phone number already exists",
                            "value": {"detail": "Такой номер телефона уже существует."},
                        },
                    }
                }
            },
        },
        500: {"model": response.ServerErrorResponseSchema},
    }


GET_RESPONSES = {
        200: {"model": ProfileResponseSchema},
        401: {"model": response.UnauthorizedResponseSchema},
        403: {"model": response.ForbiddenResponseSchema},
        404: {"model": response.NotFoundResponseSchema},
        500: {"model": response.ServerErrorResponseSchema},
    }
