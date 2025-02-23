from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from cache.data_for_cache import MovieFromAnotherProjectCache, MovieSmallInfoCache
from keyboards.inline import InlineKbForMovie, InlineKbForProject
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from services.history import write_history
from sqlalchemy.ext.asyncio import AsyncSession
from utils.tg.process_photo import edit_photo, send_photo


async def write_history_and_send_movie(
    session: AsyncSession,
    tg_obj: Message | CallbackQuery,
    movie: MovieSmallInfoCache,
    idx: int,
    length: int,
    cache: FSMContext,
    user_id: int | None = None,
) -> None:
    """
    Пишет информацию о фильме в историю и отправляет ее пользователю

    :param session: сессия для работы с базой
    :param tg_obj: Message или CallbackQuery
    :param movie: MovieSmallInfoCache
    :param idx: индекс фильма в кэше
    :param length: количество фильмов в кэше
    :param cache: кэш с данными
    :param user_id: id пользователя. Подставляется в базу, если передан, иначе берется из tg_obj
    :return: None
    """
    await write_history(
        session=session,
        user_id=user_id or tg_obj.from_user.id,
        movie_id=movie.movie_id,
        text=movie.text,
        url=movie.photo,
    )
    markup = await InlineKbForMovie.get_kb_to_switch_movie_and_view_details(
        movie_id=movie.movie_id,
        idx=idx,
        length=length,
        cache=cache,
    )

    if isinstance(tg_obj, CallbackQuery):
        await edit_photo(
            callback=tg_obj, text=movie.text, photo=movie.photo, markup=markup
        )
        return
    await send_photo(message=tg_obj, text=movie.text, photo=movie.photo, markup=markup)


async def write_history_and_send_related_movie(
    session: AsyncSession,
    callback: CallbackQuery,
    cache: FSMContext,
    project: MovieFromAnotherProjectCache,
    callback_data: MovieBackCbData,
    title: str,
    length: int,
) -> None:
    """
    Пишет информацию о фильме, связанным с текущим, в историю и отправляет ее пользователю
    :param session: сессия для работы с базой
    :param callback: CallbackQuery
    :param cache: кэш с данными
    :param project: MovieFromAnotherProjectCache
    :param callback_data: MovieBackCbData
    :param title: название фильма
    :param length: количество фильмов в кэше
    :return: None
    """

    await write_history(
        session=session,
        user_id=callback.from_user.id,
        movie_id=project.movie_id,
        text=project.text,
        url=project.photo,
    )
    markup = await InlineKbForProject.get_kb_to_switch_entities(
        callback_data,
        title,
        length,
        project.movie_id,
        cache,
        project.watchability,
    )

    await edit_photo(
        callback=callback, text=project.text, photo=project.photo, markup=markup
    )
