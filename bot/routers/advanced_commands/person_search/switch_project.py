from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import MovieRelatedSearch
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.write_history import write_history_and_send_related_movie

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(
        F.options.in_(
            (
                ViewingMovieDetails.ACTOR_PROJECTS,
                ViewingMovieDetails.DIRECTOR_PROJECTS,
            )
        )
    )
)
async def handle_next_or_prev_project(
    callback: CallbackQuery,
    callback_data: MovieBackCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Переключает проекты

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    project, title, length = await MovieRelatedSearch.get_person_project_title_and_len(
        callback_data, state
    )
    await write_history_and_send_related_movie(
        session=session,
        callback=callback,
        cache=state,
        project=project,
        callback_data=callback_data,
        title=title,
        length=length,
    )
