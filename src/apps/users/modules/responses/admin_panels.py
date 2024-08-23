from common.schemas.responses import mixins as response


GET_LIST_RESPONSES = {
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenAdminResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}
