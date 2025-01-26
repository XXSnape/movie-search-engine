from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .person_details import router as person_details_router
from .switch_person import router as switch_person_router
from .switch_project import router as switch_project_router

switch_project_router.callback_query.middleware(DbSessionMiddleware())

router = Router(name=__name__)
router.include_routers(
    person_details_router, switch_person_router, switch_project_router
)
