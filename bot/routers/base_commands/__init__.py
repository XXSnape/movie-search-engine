from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .common import router as common_router
from .start import router as start_router
from .unrecognized import router as unrecognized_router

router = Router(name=__name__)

unrecognized_router.message.middleware(DbSessionMiddleware())

router.include_routers(
    start_router,
    unrecognized_router,
)
