from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.switch_movie import switch_movie

router = Router(name=__name__)


@router.callback_query(MovieBackCbData.filter(F.options == ViewingMovieDetails.MOVIES))
async def handle_next_or_prev_movie(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: MovieBackCbData,
    session: AsyncSession,
) -> None:
    """
    Переключает фильмы

    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: MovieBackCbData
    :param session: сессия для работы с базой
    :return: None
    """
    await switch_movie(
        session=session,
        callback=callback,
        cache=state,
        movie_index=callback_data.index,
    )
