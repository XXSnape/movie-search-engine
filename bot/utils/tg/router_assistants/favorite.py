from collections.abc import Iterable
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import MovieAdvancedSearch
from cache.button_cache import get_buttons_kb_data
from services.favorite import get_favorite_movies_by_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import COMMAND_CACHE, FAVORITE_IDS_CACHE
from utils.constants.error_data import NO_FAVORITE
from utils.enums.commands import Commands
from utils.tg.switch_movie import send_first_movie


async def handle_favorite(
    session: AsyncSession,
    callback: CallbackQuery,
    cache: FSMContext,
    user_id: int,
) -> None:
    """
    Обрабатывает команду favorite

    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param user_id: id пользователя
    :return: None
    """
    await cache.clear()
    favorite_movies_id = await _start_favorite(
        session=session, callback=callback, cache=cache, user_id=user_id
    )
    if favorite_movies_id is None:
        return
    await send_first_movie(
        session,
        MovieAdvancedSearch.get_movies_and_len_by_ids,
        callback,
        cache,
        text=NO_FAVORITE,
        ids=favorite_movies_id,
    )


async def _start_favorite(
    session: AsyncSession,
    callback: CallbackQuery,
    cache: FSMContext,
    user_id: int,
) -> Iterable[int] | None:
    """
    Обрабатывает id фильмов в избранном, если они есть
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param user_id: id пользователя
    :return: id фильмов или None
    """
    favorite_movies_id = await get_favorite_movies_by_user_id(session, user_id)
    if not favorite_movies_id:
        await callback.answer("Нет фильмов в Избранном", show_alert=True)
        return
    await cache.update_data(
        {COMMAND_CACHE: Commands.FAVORITE, FAVORITE_IDS_CACHE: favorite_movies_id}
    )
    return favorite_movies_id


async def switch_markup(
    callback: CallbackQuery, cache: FSMContext, func: Callable, movie_id: int, text: str
) -> None:
    """
    Переключает клавиатуру после манипуляций с избранным
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param func: функция для генерации новой клавиатуры
    :param movie_id: id фильма
    :param text: текст для ответа
    :return: None
    """
    all_buttons, favorite_index, sizes = await get_buttons_kb_data(cache=cache)
    markup = func(
        all_buttons=all_buttons,
        favorite_index=favorite_index,
        sizes=sizes,
        movie_id=movie_id,
    )
    await callback.answer(text, show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=markup)
