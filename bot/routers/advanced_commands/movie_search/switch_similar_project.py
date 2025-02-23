from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.switch_movie import switch_related_project

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(F.options == ViewingMovieDetails.SIMILAR_PROJECTS)
)
async def handle_next_or_prev_similar_project(
    callback: CallbackQuery,
    callback_data: MovieBackCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Переключает похожие фильмы

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    await switch_related_project(
        session, callback, callback_data, state, "similar_projects"
    )
