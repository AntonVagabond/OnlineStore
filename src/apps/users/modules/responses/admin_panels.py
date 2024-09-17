from common.schemas.responses import mixins as response

GET_LIST_RESPONSES = {
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenAdminResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}

GET_RESPONSES = {
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenAdminResponseSchema},
    404: {"model": response.UserNotFoundResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}

EDIT_RESPONSES = {
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": True}},
    },
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenAdminResponseSchema},
    404: {"model": response.UserNotFoundResponseSchema},
}

DELETE_RESPONSES = {
    204: {
        "description": "Successful Response",
        "content": {"application/json": {"example": {}}},
    },
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenAdminResponseSchema},
    404: {"model": response.UserNotFoundResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}
