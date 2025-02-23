from aiogram import Router

from .start_movie_by_statuses import router as movie_by_statuses_router

router = Router()

router.include_routers(movie_by_statuses_router)
