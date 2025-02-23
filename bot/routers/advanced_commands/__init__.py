from aiogram import Router

from .favorite import router as favorite_router
from .history import router as history_router
from .movie_by_collections import router as movie_by_collections_router
from .movie_by_params import router as movie_by_params_router
from .movie_by_statuses import router as movie_by_statuses_router
from .movie_in_cinema import router as movie_in_cinema_router
from .movie_search import router as movie_search_router
from .person_search import router as person_search_router
from .requests import router as requests_router
from .review_search import router as review_search_router
from .survey import router as survey_router

router = Router(name=__name__)
router.include_routers(
    movie_search_router,
    person_search_router,
    movie_by_params_router,
    movie_by_statuses_router,
    movie_in_cinema_router,
    movie_by_collections_router,
    review_search_router,
    survey_router,
    favorite_router,
    history_router,
    requests_router,
)
