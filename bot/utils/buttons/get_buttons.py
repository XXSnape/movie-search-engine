from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.data_for_cache import MovieBigInfoCache
from cache.get_data import get_data_from_cache
from keyboards.inline.buttons.movie import get_buttons_for_back_to_movies
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.related_project_kb import InlineKbForProject


async def get_buttons_for_back_by_callback(
    callback_data: MovieBackCbData, cache: FSMContext
) -> list[InlineKeyboardButton]:
    """
    Возвращает кнопки для перехода к фильмам по callback
    :param callback_data: MovieBackCbData
    :param cache: кэш с данными
    :return: list[InlineKeyboardButton]
    """
    movie = await get_data_from_cache(str(callback_data.movie_id), cache=cache)
    return get_buttons_for_back_to_movies(callback_data, movie.title)


async def get_buttons_for_switch_by_callback(
    data_for_back: MovieBackCbData, cache: FSMContext, length: int
) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для переключения отзывов

    :param data_for_back: MovieBackCbData
    :param cache: кэш с данными
    :param length: количество отзывов
    :return: InlineKeyboardMarkup
    """
    movie: MovieBigInfoCache = await get_data_from_cache(
        str(data_for_back.movie_id), cache=cache
    )
    return await InlineKbForProject.get_kb_to_switch_entities(
        data_for_back=data_for_back,
        title=movie.title,
        length=length,
        movie_id=movie.movie_id,
        cache=cache,
    )
