from aiogram import Router
from middlewares.db import DbSessionMiddleware

from .download_movie import router as download_movie_router
from .invalid_input import router as invalid_input_router
from .movie_details import router as movie_details_router
from .movie_title import router as movie_title_router
from .start_movie_search import router as movie_search_router
from .switch_movie import router as switch_movie_router
from .switch_sequel import router as switch_sequel_router
from .switch_similar_project import router as switch_similar_project_router

movie_title_router.message.middleware(DbSessionMiddleware())
switch_movie_router.callback_query.middleware(DbSessionMiddleware())
switch_sequel_router.callback_query.middleware(DbSessionMiddleware())
switch_similar_project_router.callback_query.middleware(DbSessionMiddleware())
download_movie_router.callback_query.middleware(DbSessionMiddleware())

router = Router(name=__name__)
router.include_routers(
    movie_search_router,
    movie_title_router,
    invalid_input_router,
    movie_details_router,
    download_movie_router,
    switch_movie_router,
    switch_sequel_router,
    switch_similar_project_router,
)
