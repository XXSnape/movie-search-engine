from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import ReviewSearch
from cache.button_cache import get_data_from_buttons
from cache.get_data import get_data_from_cache
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.buttons import ParseDataFromCb
from utils.buttons.get_buttons import get_buttons_for_switch_by_callback
from utils.constants.cache_keys import CALLBACK_DATA_CACHE
from utils.enums.movie_data import ViewingMovieDetails
from utils.survey_data import RUSSIAN_TYPES_REVIEWS


async def send_first_review(callback: CallbackQuery, cache: FSMContext) -> None:
    """
    Отправляет отзыв

    :param callback: CallbackQuery
    :param cache: кэш с данными
    :return: None
    """
    data_for_back: MovieBackCbData = await get_data_from_cache(
        CALLBACK_DATA_CACHE, cache=cache
    )
    types = await get_data_from_buttons(
        cache=cache, get_cb=ParseDataFromCb(RUSSIAN_TYPES_REVIEWS)
    )
    info = await ReviewSearch.get_reviews_and_len_by_params(
        cache=cache, types=types, movie_id=data_for_back.movie_id
    )
    if info is None:
        await callback.answer("Не нашлось ни одного отзыва.", show_alert=True)
        return
    data_for_back.options = ViewingMovieDetails.VIEWING_REVIEWS
    await cache.set_state(None)
    text, length = info
    markup = await get_buttons_for_switch_by_callback(data_for_back, cache, length)
    await callback.message.edit_text(text=text, reply_markup=markup)
