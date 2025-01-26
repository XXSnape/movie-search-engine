from aiogram import Router

from .advanced_commands import router as advanced_commands_router
from .base_commands import common_router
from .base_commands import router as base_commands_router

router = Router(name=__name__)
router.include_routers(
    common_router,
    advanced_commands_router,
    base_commands_router,
)
