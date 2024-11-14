from typing import Annotated

from fastapi import Cookie, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from api.current_user_deps import CurrentUserDep
from clients.users import UserClientService
from common.interfaces.abstraction_uow import IUnitOfWork
from core.config import settings
from core.constants import REFRESH
from modules.schemas.auth_schema import EmptyUserSchema
from modules.services.auth_service import AuthUserService
from modules.unit_of_works.auth_uow import AuthUOW

UserDep = Annotated[EmptyUserSchema, Depends(CurrentUserDep.get_current_user())]
AuthUOWDep = Annotated[IUnitOfWork, Depends(AuthUOW)]
AuthUserServiceDep = Annotated[AuthUserService, Depends(AuthUserService)]


def get_user_client_service() -> UserClientService:
    """Получить клиентский сервис пользователя."""
    return UserClientService(str(settings.auth.user_endpoint_url))


UserClientServiceDep = Annotated[UserClientService, Depends(get_user_client_service)]
OAuth2PasswordDep = Annotated[OAuth2PasswordRequestForm, Depends()]
RefreshDep = Annotated[str, Cookie(alias=REFRESH, include_in_schema=False)]
TokenDep = Annotated[str, Header()]
RolesDep = Annotated[tuple[str, ...], Header()]
HeadersDep = Annotated[str, Header(...)]
