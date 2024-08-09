from typing import Annotated

from fastapi import Depends

from common.interfaces.abstraction_uow import IUnitOfWork
from common.schemas.api.mixins import CurrentUserSchema
from common.services.base import BaseService
from core.security import get_current_user
from modules.services.profiles import ProfileService
from modules.unit_of_works.profiles import ProfileUOW

# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[CurrentUserSchema, Depends(get_current_user())]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- PROFILE ---------------------------------------
ProfileUOWDep = Annotated[IUnitOfWork, Depends(ProfileUOW)]
ProfileServiceDep = Annotated[BaseService, Depends(ProfileService)]
# endregion ------------------------------------------------------------------------------
