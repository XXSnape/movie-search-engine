from aiogram import Router

from .start_movie_by_params import router as movie_by_params_router

router = Router(name=__name__)

router.include_routers(
    movie_by_params_router,
)
