from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .actions_with_request import router as actions_with_request_router
from .save_request import router as save_request_router
from .start_requests import router as start_requests_router
from .switch_request import router as switch_request_router

actions_with_request_router.callback_query.middleware(DbSessionMiddleware())
start_requests_router.callback_query.middleware(DbSessionMiddleware())
start_requests_router.message.middleware(DbSessionMiddleware())
save_request_router.callback_query.middleware(DbSessionMiddleware())


router = Router()
router.include_routers(
    start_requests_router,
    actions_with_request_router,
    save_request_router,
    switch_request_router,
)
