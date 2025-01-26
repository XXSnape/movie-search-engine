from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from api import MovieSearch
from config.settings import settings
from services.favorite import get_favorite_movies_by_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from states.movie_search import SearchMovieByTitleFSM
from utils.constants.cache_keys import (
    COMMAND_CACHE,
    FAVORITE_IDS_CACHE,
    MIN_PAGE_CACHE,
    PARAMS_CACHE,
)
from utils.enums.commands import Commands
from utils.tg.switch_movie import send_first_movie

router = Router(name=__name__)


@router.message(SearchMovieByTitleFSM.title, F.text)
@flags.chat_action("typing")
async def handle_title_of_movie(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает название фильма

    :param message: Message
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    favorite_ids = await get_favorite_movies_by_user_id(
        session=session, user_id=message.from_user.id
    )
    params = {"page": 1, "limit": settings.API.NUMBER_FILMS, "query": message.text}
    await state.update_data(
        {
            PARAMS_CACHE: params,
            COMMAND_CACHE: Commands.MOVIE_SEARCH,
            MIN_PAGE_CACHE: 1,
            FAVORITE_IDS_CACHE: favorite_ids,
        }
    )
    await send_first_movie(
        session=session,
        func=MovieSearch.get_movie_and_length_by_title,
        tg_obj=message,
        cache=state,
        params=params,
    )
