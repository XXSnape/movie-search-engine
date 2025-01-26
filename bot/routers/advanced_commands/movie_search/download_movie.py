from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config.settings import settings
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.router_assistants.movie import set_new_page
from utils.tg.write_history import write_history_and_send_movie

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(
        F.options.in_(
            (
                ViewingMovieDetails.DOWNLOAD_PREVIOUS,
                ViewingMovieDetails.DOWNLOAD_FOLLOWING,
            )
        )
    )
)
async def handle_movie_download(
    callback: CallbackQuery,
    callback_data: MovieBackCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Обрабатывает подгрузку фильмов.
    Если пользователь просмотрел NUMBER_FILMS на странице, загружается новая страница.
    Если просмотрел фильм под индексом 0 в кэше, загружается предыдущая страница,
    и индекс в кэше становится равен NUMBER_FILMS - 1

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    movie, length = await set_new_page(cache=state, callback_data=callback_data)
    await write_history_and_send_movie(
        session=session,
        tg_obj=callback,
        movie=movie,
        idx=(
            callback_data.index + 1
            if callback_data.options == ViewingMovieDetails.DOWNLOAD_FOLLOWING
            else settings.API.NUMBER_FILMS - 1
        ),
        length=length,
        cache=state,
    )
