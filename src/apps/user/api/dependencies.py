from typing import Annotated

from fastapi import Depends

from common.interfaces.abstraction_uow import IUnitOfWork
from common.schemas.api.mixins import CurrentUserSchema
from common.services.base import BaseService
from common.unit_of_works.base import BaseUnitOfWork
from core.security import get_current_user
from modules.repositories.profiles import ProfileRepository
from modules.services.profiles import ProfileService
from modules.unit_of_works.profiles import ProfileUOW

# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[CurrentUserSchema, Depends(get_current_user())]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- PROFILE ---------------------------------------
ProfileUOWDep = Annotated[ProfileUOW, Depends(ProfileUOW)]
ProfileServiceDep = Annotated[ProfileService, Depends(ProfileService)]
# endregion ------------------------------------------------------------------------------
