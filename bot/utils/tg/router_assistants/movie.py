from logging import getLogger

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from api import MediaSearch, MovieAdvancedSearch, MovieSearch
from cache.data_for_cache import MovieSmallInfoCache
from keyboards.inline import InlineKbForMovie, InlineKbForSurvey
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.constants.cache_keys import COMMAND_CACHE, MIN_PAGE_CACHE, PARAMS_CACHE
from utils.constants.error_data import NO_FRAMES
from utils.enums.commands import Commands
from utils.enums.movie_data import ViewingMovieDetails

logger = getLogger(name=__name__)


async def handle_collections(message: Message, cache: FSMContext) -> None:
    await cache.clear()
    markup = InlineKbForSurvey.get_kb_with_collections_categories()
    await message.answer("Выберете интересующую категорию", reply_markup=markup)


async def set_new_page(
    cache: FSMContext, callback_data: MovieBackCbData
) -> tuple[MovieSmallInfoCache, int] | None:
    """
    Обновляет информацию об интересующей странице в параметрах запроса в зависимости от типа подгрузки.
    В кэше сохраняет информацию о наименьшей просмотренной странице для дальнейшего сохранения запроса.

    :param cache: кэш с данными
    :param callback_data: MovieBackCbData
    :return: tuple[MovieSmallInfoCache, int] или None
    """
    data = await cache.get_data()
    command = data[COMMAND_CACHE]
    params = data[PARAMS_CACHE]
    params["page"] += (
        1 if callback_data.options == ViewingMovieDetails.DOWNLOAD_FOLLOWING else -1
    )
    await cache.update_data(
        {
            MIN_PAGE_CACHE: min(
                [
                    params["page"],
                    data[MIN_PAGE_CACHE],
                ]
            )
        },
    )
    if command == Commands.MOVIE_SEARCH:
        api = MovieSearch.get_movie_and_length_by_title
    else:
        api = MovieAdvancedSearch.get_movies_and_len_by_advanced_params
    return await api(cache=cache, params=params, download_type=callback_data.options)


async def send_pictures(
    callback: CallbackQuery, cache: FSMContext, callback_data: MovieBackCbData
) -> None:
    """
    Отправляет кадры из фильма
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param callback_data: MovieBackCbData
    :return: None
    """
    pictures = await MediaSearch.get_photos_by_id(movie_id=callback_data.movie_id)
    if not pictures:
        await callback.answer(NO_FRAMES, show_alert=True)
        return
    try:
        await callback.bot.send_media_group(
            chat_id=callback.from_user.id, media=pictures
        )
    except TelegramBadRequest:
        logger.exception("Не удалось отправить все кадры из фильма")
        await callback.answer(NO_FRAMES, show_alert=True)
        return
    await callback.message.delete()
    movie = await MovieSearch.get_movie_by_id(
        movie_id=callback_data.movie_id, cache=cache
    )
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=movie.text,
        reply_markup=await InlineKbForMovie.get_kb_for_movie_details(
            data_for_back=callback_data, movie=movie, cache=cache
        ),
    )
