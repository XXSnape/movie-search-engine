from aiogram import Router

from .start_movie_in_cinema import router as movie_in_cinema_router

router = Router()
router.include_routers(movie_in_cinema_router)
