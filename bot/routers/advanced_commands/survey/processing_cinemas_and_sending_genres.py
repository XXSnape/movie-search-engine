from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.fill_in_cache import fill_in_params_on_key
from states.movie_search import SearchMovieByDataFSM
from utils.buttons.parse_cb_data import ParseDataFromCb
from utils.constants.api_data import CINEMA_KEY
from utils.constants.output_for_user import GENRE_OUTPUT
from utils.constants.router_keys import ANY_PLATFORM_ROUTER, END_ROUTER
from utils.survey_data import API_CINEMAS
from utils.survey_data.cinemas import ADDITIONAL_CINEMAS
from utils.tg.router_assistants.survey import (
    move_to_new_stage,
    save_info_and_move_to_new_stage,
)

router = Router(name=__name__)


@router.callback_query(SearchMovieByDataFSM.cinemas, F.data == END_ROUTER)
async def handle_cinemas_and_send_genres_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает онлайн-кинотеатры и отправляет жанры на выбор
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await save_info_and_move_to_new_stage(
        callback=callback,
        cache=state,
        key=CINEMA_KEY,
        parse_data=ParseDataFromCb(storage=API_CINEMAS),
        data_fsm=SearchMovieByDataFSM.genres,
        text=GENRE_OUTPUT,
    )


@router.callback_query(SearchMovieByDataFSM.cinemas, F.data == ANY_PLATFORM_ROUTER)
async def handle_all_cinemas_and_send_genres_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает кнопку "Любая платформа" и отправляет жанры на выбор
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    cinemas = API_CINEMAS + ADDITIONAL_CINEMAS
    await fill_in_params_on_key(key=CINEMA_KEY, data=cinemas, cache=state)
    await move_to_new_stage(
        callback=callback,
        cache=state,
        data_fsm=SearchMovieByDataFSM.genres,
        text=GENRE_OUTPUT,
    )
