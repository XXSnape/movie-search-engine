from re import Match

from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from api import MovieAdvancedSearch
from cache.fill_in_cache import fill_in_params_on_key
from cache.get_data import get_data_from_cache
from keyboards.reply.survey_kb import ReplyKbForSurvey
from services.favorite import get_favorite_movies_by_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from states.movie_search import SearchMovieByDataFSM
from utils.constants.cache_keys import FAVORITE_IDS_CACHE, MIN_PAGE_CACHE, PARAMS_CACHE
from utils.constants.router_keys import ANY_YEAR_ROUTER
from utils.response_formats import TEXT_OVER_YEARS
from utils.tg.switch_movie import send_first_movie

router = Router()


@router.message(
    SearchMovieByDataFSM.years, F.text.regexp(r"^(\d{4})$|^(\d{4} \d{4})$").as_("years")
)
@flags.chat_action("typing")
async def handle_years_end_sending_movie(
    message: Message, state: FSMContext, session: AsyncSession, years: Match[str]
) -> None:
    """
    Обрабатывает годы по шаблону YYYY или YYYY YYYY и отправляет фильм
    :param message: Message
    :param state: FSMContext
    :param session: сессия для работы с базой
    :param years: выбранные годы
    :return: None
    """
    favorite_ids = await get_favorite_movies_by_user_id(
        session=session, user_id=message.from_user.id
    )
    year = years.group().replace(" ", "-")
    params = await fill_in_params_on_key(key="year", data=year, cache=state)
    await state.update_data({MIN_PAGE_CACHE: 1, FAVORITE_IDS_CACHE: favorite_ids})
    await send_first_movie(
        session=session,
        func=MovieAdvancedSearch.get_movies_and_len_by_advanced_params,
        cache=state,
        tg_obj=message,
        params=params,
    )


@router.message(
    SearchMovieByDataFSM.years,
    F.text == ANY_YEAR_ROUTER,
)
@flags.chat_action("typing")
async def handle_absence_years_and_send_movie(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает кнопку "Любой год" и отправляет фильм

    :param message: Message
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    favorite_ids = await get_favorite_movies_by_user_id(
        session=session, user_id=message.from_user.id
    )
    params = await get_data_from_cache(PARAMS_CACHE, cache=state)
    await state.update_data({MIN_PAGE_CACHE: 1, FAVORITE_IDS_CACHE: favorite_ids})
    await send_first_movie(
        session=session,
        func=MovieAdvancedSearch.get_movies_and_len_by_advanced_params,
        cache=state,
        tg_obj=message,
        params=params,
    )


@router.message(
    SearchMovieByDataFSM.years,
)
async def handle_invalid_years(message: Message) -> None:
    """
    Обрабатывает невалидный ввод года

    :param message: Message
    :return: None
    """
    markup = ReplyKbForSurvey.get_kb_for_select_years()
    await message.reply(
        text="Неверный формат данных\n\n" + TEXT_OVER_YEARS, reply_markup=markup
    )
