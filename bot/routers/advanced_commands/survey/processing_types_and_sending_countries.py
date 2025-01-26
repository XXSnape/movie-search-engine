from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.buttons import ParseDataFromCb
from utils.constants.api_data import TYPE_KEY
from utils.constants.output_for_user import COUNTRY_OUTPUT
from utils.constants.router_keys import END_ROUTER
from utils.survey_data import API_TYPES
from utils.tg.router_assistants.survey import save_info_and_move_to_new_stage

router = Router()


@router.callback_query(SearchMovieByDataFSM.types, F.data == END_ROUTER)
async def handle_types_and_send_countries_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает типы фильмов и отправляет страны на выбор

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await save_info_and_move_to_new_stage(
        callback=callback,
        cache=state,
        key=TYPE_KEY,
        parse_data=ParseDataFromCb(storage=API_TYPES),
        data_fsm=SearchMovieByDataFSM.countries,
        text=COUNTRY_OUTPUT,
    )
