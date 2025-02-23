from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .processing_cinemas_and_sending_movie import (
    router as cinemas_and_send_movie_router,
)
from .start_movie_by_collections import router as start_movie_by_collections_router
from .survey_on_collections import router as survey_on_collections_router

cinemas_and_send_movie_router.callback_query.middleware(DbSessionMiddleware())

router = Router()
router.include_routers(
    survey_on_collections_router,
    cinemas_and_send_movie_router,
    start_movie_by_collections_router,
)
