from aiogram import Router

from .select_types_reviews import router as select_types_reviews_router
from .switch_review import router as switch_review_router

router = Router()
router.include_routers(select_types_reviews_router, switch_review_router)
