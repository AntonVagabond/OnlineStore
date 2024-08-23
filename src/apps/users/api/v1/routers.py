from .controllers.admin_panels import admin_panel as admin_panel_router
from .controllers.profiles import profile as profile_router

all_routers_v1 = (
    admin_panel_router, profile_router
)
