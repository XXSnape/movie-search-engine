from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .start_favorite import router as start_favorite_router
from .switch_favorite_movies import router as switch_favorite_movies_router

start_favorite_router.message.middleware(DbSessionMiddleware())
start_favorite_router.callback_query.middleware(DbSessionMiddleware())

switch_favorite_movies_router.callback_query.middleware(DbSessionMiddleware())

router = Router()
router.include_routers(switch_favorite_movies_router, start_favorite_router)
