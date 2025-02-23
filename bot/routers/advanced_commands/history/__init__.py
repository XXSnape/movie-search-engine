from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .calendar import router as calendar_router
from .delete_history import router as delete_history_router
from .select_type_of_deletion import router as select_type_deletion_router
from .send_history import router as send_history_router
from .start_history import router as start_history_router
from .switch_history import router as switch_history_router

start_history_router.message.middleware(DbSessionMiddleware())
start_history_router.callback_query.middleware(DbSessionMiddleware())
send_history_router.callback_query.middleware(DbSessionMiddleware())
delete_history_router.callback_query.middleware(DbSessionMiddleware())


router = Router()
router.include_routers(
    start_history_router,
    send_history_router,
    select_type_deletion_router,
    calendar_router,
    switch_history_router,
    delete_history_router,
)
