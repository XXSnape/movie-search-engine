from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.buttons.parse_cb_data import ParseDataFromCb
from utils.constants.api_data import STATUS_KEY
from utils.constants.output_for_user import GENRE_OUTPUT
from utils.constants.router_keys import END_ROUTER
from utils.survey_data import API_STATUSES
from utils.tg.router_assistants.survey import save_info_and_move_to_new_stage

router = Router(name=__name__)


@router.callback_query(SearchMovieByDataFSM.statuses, F.data == END_ROUTER)
async def handle_statuses_and_send_genres_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает статусы и отправляет жанры на выбор

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await save_info_and_move_to_new_stage(
        callback=callback,
        cache=state,
        key=STATUS_KEY,
        parse_data=ParseDataFromCb(storage=API_STATUSES),
        data_fsm=SearchMovieByDataFSM.genres,
        text=GENRE_OUTPUT,
    )
