from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .edit_kb_when_pressed import router as edit_kb_router
from .processing_cinemas_and_sending_genres import router as cinemas_and_genres_router
from .processing_countries_and_requesting_years import (
    router as counties_and_years_router,
)
from .processing_genres_and_sending_types import router as genres_and_types_router
from .processing_networks_and_sending_cinemas import (
    router as networks_and_cinemas_router,
)
from .processing_statuses_and_sending_genres import router as statuses_and_genres_router
from .processing_types_and_sending_countries import router as types_and_countries_router
from .processing_years_and_sending_movie import router as years_and_send_movie_router

years_and_send_movie_router.message.middleware(DbSessionMiddleware())

router = Router()
router.include_routers(
    edit_kb_router,
    counties_and_years_router,
    years_and_send_movie_router,
    types_and_countries_router,
    genres_and_types_router,
    statuses_and_genres_router,
    cinemas_and_genres_router,
    networks_and_cinemas_router,
)
