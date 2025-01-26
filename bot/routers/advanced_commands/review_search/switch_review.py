from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_data_from_cache
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.buttons.get_buttons import get_buttons_for_switch_by_callback
from utils.constants.cache_keys import REVIEWS_CACHE
from utils.enums.movie_data import ViewingMovieDetails

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(F.options == ViewingMovieDetails.VIEWING_REVIEWS)
)
async def handle_next_or_prev_review(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Переключает отзывы

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    reviews = await get_data_from_cache(REVIEWS_CACHE, cache=state)
    markup = await get_buttons_for_switch_by_callback(
        callback_data, state, len(reviews)
    )
    await callback.message.edit_text(
        text=reviews[callback_data.related_entity_index], reply_markup=markup
    )
