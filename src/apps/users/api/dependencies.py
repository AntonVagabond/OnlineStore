from typing import Annotated

from fastapi import Depends

from clients.auth import get_current_user
from common.schemas.api.mixins import CurrentUserSchema
from modules.schemas.admin_panels import UserByRoleFilterSchema
from modules.services.admin_panels import AdminPanelService
from modules.services.profiles import ProfileService
from modules.unit_of_works.admin_panels import AdminPanelUOW
from modules.unit_of_works.profiles import ProfileUOW

# region ---------------------------------- COMMON ---------------------------------------
UserSchemaDep = Annotated[CurrentUserSchema, Depends(get_current_user())]
# endregion ------------------------------------------------------------------------------

# region --------------------------------- PROFILE ---------------------------------------
ProfileUOWDep = Annotated[ProfileUOW, Depends(ProfileUOW)]
ProfileServiceDep = Annotated[ProfileService, Depends(ProfileService)]
# endregion ------------------------------------------------------------------------------


# region ----------------------------- ADMIN PANEL ---------------------------------------
AdminDep = Depends(get_current_user(("admin",)))
AdminSchemaDep = Annotated[CurrentUserSchema, Depends(get_current_user(("admin",)))]
AdminPanelUOWDep = Annotated[AdminPanelUOW, Depends(AdminPanelUOW)]
AdminPanelServiceDep = Annotated[AdminPanelService, Depends(AdminPanelService)]
UserByRoleFilterDep = Annotated[UserByRoleFilterSchema, Depends(UserByRoleFilterSchema)]
# endregion ------------------------------------------------------------------------------
