from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_data_from_cache
from sqlalchemy.ext.asyncio import AsyncSession
from states.movie_search import SearchMovieByDataFSM
from utils.buttons import ParseDataFromCb
from utils.constants.api_data import CINEMA_KEY
from utils.constants.cache_keys import PARAMS_CACHE
from utils.constants.router_keys import ANY_PLATFORM_ROUTER, END_ROUTER
from utils.survey_data import API_CINEMAS
from utils.survey_data.cinemas import ADDITIONAL_CINEMAS
from utils.tg.router_assistants.survey import save_info_to_cache
from utils.tg.switch_movie import send_movie_by_collections

router = Router(name=__name__)


@router.callback_query(SearchMovieByDataFSM.collection_cinemas, F.data == END_ROUTER)
async def handle_cinemas_and_send_movie(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает онлайн-кинотеатры и отправляет фильм
    :param callback: CallbackQuery
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    await save_info_to_cache(
        cache=state,
        key=CINEMA_KEY,
        parse_data=ParseDataFromCb(storage=API_CINEMAS),
    )
    params = await get_data_from_cache(PARAMS_CACHE, cache=state)

    await send_movie_by_collections(
        session=session, callback=callback, cache=state, params=params
    )


@router.callback_query(
    SearchMovieByDataFSM.collection_cinemas, F.data == ANY_PLATFORM_ROUTER
)
async def handle_all_cinemas_and_send_movie(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает кнопку "Любая платформа" и отправляет фильм
    :param callback: CallbackQuery
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    params = await get_data_from_cache(PARAMS_CACHE, cache=state)
    params[CINEMA_KEY] = API_CINEMAS + ADDITIONAL_CINEMAS

    await send_movie_by_collections(
        session=session, callback=callback, cache=state, params=params
    )
