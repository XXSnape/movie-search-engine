from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.movie_factory import FavoriteMovieCbData
from keyboards.inline.keyboards.favorite_kb import InlineKbForFavorite
from services.favorite import add_movie_to_favorite, delete_movie_from_favorite
from sqlalchemy.ext.asyncio import AsyncSession
from utils.constants.output_for_user import SUCCESSFULLY_OUTPUT
from utils.enums.favorite_data import SelectActionWithFavorite
from utils.tg.router_assistants.favorite import switch_markup

router = Router(name=__name__)


@router.callback_query(
    FavoriteMovieCbData.filter(F.options == SelectActionWithFavorite.ADD)
)
async def handle_addiction_to_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: FavoriteMovieCbData,
    session: AsyncSession,
) -> None:
    """
    Добавляет фильм в избранное
    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: FavoriteMovieCbData
    :param session: сессия для работы с базой
    :return: None
    """
    await add_movie_to_favorite(
        session=session,
        user_id=callback.from_user.id,
        movie_id=callback_data.movie_id,
        cache=state,
    )
    await switch_markup(
        callback=callback,
        cache=state,
        func=InlineKbForFavorite.replace_addition_with_deletion,
        movie_id=callback_data.movie_id,
        text=f"Фильм успешно добавлен в Избранное!{SUCCESSFULLY_OUTPUT}",
    )


@router.callback_query(
    FavoriteMovieCbData.filter(F.options == SelectActionWithFavorite.DELETE)
)
async def handle_deleting_from_favorite(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: FavoriteMovieCbData,
    session: AsyncSession,
) -> None:
    """
    Удаляет фильм из избранного
    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: FavoriteMovieCbData
    :param session: сессия для работы с базой
    :return: None
    """
    await delete_movie_from_favorite(
        session=session,
        cache=state,
        user_id=callback.from_user.id,
        movie_id=callback_data.movie_id,
    )
    await switch_markup(
        callback=callback,
        cache=state,
        func=InlineKbForFavorite.replace_deletion_with_addition,
        movie_id=callback_data.movie_id,
        text=f"Фильм успешно удален из Избранных{SUCCESSFULLY_OUTPUT}",
    )
