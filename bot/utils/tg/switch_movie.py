from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from api import MovieAdvancedSearch, MovieCache, MovieRelatedSearch
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from services.favorite import get_favorite_movies_by_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.cache_keys import FAVORITE_IDS_CACHE
from utils.constants.error_data import NOT_FOUND
from utils.tg.write_history import (
    write_history_and_send_movie,
    write_history_and_send_related_movie,
)


async def send_first_movie(
    session: AsyncSession,
    func: Callable,
    tg_obj: Message | CallbackQuery,
    cache: FSMContext,
    text: str = NOT_FOUND,
    idx: int = 0,
    user_id: int | None = None,
    **kwargs
) -> None:
    """
    Отправляет фильм после опроса и получения всех данных

    :param session: сессия для работы с базой
    :param func: функция, которая обращается к api
    :param tg_obj: Message или CallbackQuery
    :param cache: кэш с данными
    :param text: текст на случай, если придет невалидный ответ от api
    :param idx: начальный индекс фильма
    :param user_id: id пользователя
    :param kwargs: дополнительные параметры для func
    :return:
    """
    info = await func(**kwargs, cache=cache)
    await cache.set_state(None)
    if info is None:
        await tg_obj.answer(
            text,
            reply_markup=InlineKbForCommand.get_kb_to_select_command(),
        )
        await cache.clear()
        return
    movie, length = info
    await write_history_and_send_movie(
        session=session,
        tg_obj=tg_obj,
        movie=movie,
        idx=idx,
        length=length,
        cache=cache,
        user_id=user_id,
    )


async def switch_movie(
    callback: CallbackQuery,
    cache: FSMContext,
    session: AsyncSession,
    movie_index: int,
) -> None:
    """
    Переключает фильм
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param session: сессия для работы с базой
    :param movie_index: индекс фильма
    :return: None
    """
    movie, length = await MovieCache.get_small_info_movie_and_length_by_idx(
        cache=cache, idx=movie_index
    )
    await write_history_and_send_movie(
        session=session,
        tg_obj=callback,
        movie=movie,
        idx=movie_index,
        length=length,
        cache=cache,
    )


async def switch_related_project(
    session: AsyncSession,
    callback: CallbackQuery,
    callback_data: MovieBackCbData,
    cache: FSMContext,
    attribute: str,
) -> None:
    """
    Переключает фильм, связанный с текущим
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param cache: кэш с данными
    :param attribute: аттрибут для обращения к объекту из кэша
    :return: None
    """
    project, title, length = (
        await MovieRelatedSearch.get_related_projects_title_and_len(
            attribute, callback_data, cache
        )
    )
    await write_history_and_send_related_movie(
        session=session,
        callback=callback,
        cache=cache,
        project=project,
        callback_data=callback_data,
        title=title,
        length=length,
    )


async def send_movie_by_collections(
    session: AsyncSession, callback: CallbackQuery, cache: FSMContext, params: dict
) -> None:
    """
    Отправляет фильм после выбора коллекция
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param params: дополнительные параметры для запроса
    :return: None
    """
    favorite_ids = await get_favorite_movies_by_user_id(
        session=session, user_id=callback.from_user.id
    )

    msg = callback.message
    await cache.set_state(None)
    await cache.update_data({FAVORITE_IDS_CACHE: favorite_ids})
    await callback.message.delete()
    await send_first_movie(
        session=session,
        func=MovieAdvancedSearch.get_movies_and_len_by_advanced_params,
        cache=cache,
        tg_obj=msg,
        params=params,
        user_id=callback.from_user.id,
    )
