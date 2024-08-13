from typing import Annotated

from fastapi import Depends

from api.current_user_deps import get_current_user
from common.schemas.api.mixins import CurrentUserSchema
from modules.services.profiles import ProfileService
from modules.unit_of_works.profiles import ProfileUOW

# region ---------------------------------- COMMON ---------------------------------------
UserDep = Annotated[CurrentUserSchema, Depends(get_current_user())]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- PROFILE ---------------------------------------
ProfileUOWDep = Annotated[ProfileUOW, Depends(ProfileUOW)]
ProfileServiceDep = Annotated[ProfileService, Depends(ProfileService)]
# endregion ------------------------------------------------------------------------------
