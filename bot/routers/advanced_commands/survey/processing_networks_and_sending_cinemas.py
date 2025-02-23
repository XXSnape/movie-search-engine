from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.buttons.parse_cb_data import ParseDataFromCb
from utils.constants.api_data import NETWORK_KEY
from utils.constants.output_for_user import ONLINE_CINEMA_OUTPUT
from utils.constants.router_keys import END_ROUTER
from utils.survey_data import API_NETWORKS
from utils.tg.router_assistants.survey import save_info_and_move_to_new_stage

router = Router(name=__name__)


@router.callback_query(SearchMovieByDataFSM.networks, F.data == END_ROUTER)
async def handle_networks_and_send_cinemas_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает сети производителей и отправляет онлайн-кинотеатры на выбор

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await save_info_and_move_to_new_stage(
        callback=callback,
        cache=state,
        key=NETWORK_KEY,
        parse_data=ParseDataFromCb(storage=API_NETWORKS),
        data_fsm=SearchMovieByDataFSM.cinemas,
        text=ONLINE_CINEMA_OUTPUT,
    )
