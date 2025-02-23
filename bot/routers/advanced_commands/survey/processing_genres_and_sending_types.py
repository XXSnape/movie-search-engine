from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.buttons import ParseDataFromCb
from utils.constants.api_data import GENRE_KEY
from utils.constants.output_for_user import TYPE_OUTPUT
from utils.constants.router_keys import END_ROUTER
from utils.survey_data import RUSSIAN_GENRES
from utils.tg.router_assistants.survey import save_info_and_move_to_new_stage

router = Router(name=__name__)


@router.callback_query(SearchMovieByDataFSM.genres, F.data == END_ROUTER)
async def handle_genres_and_send_types_of_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает жанры и отправляет типы фильмов на выбор
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await save_info_and_move_to_new_stage(
        callback=callback,
        cache=state,
        key=GENRE_KEY,
        parse_data=ParseDataFromCb(storage=RUSSIAN_GENRES, func=str.lower),
        data_fsm=SearchMovieByDataFSM.types,
        text=TYPE_OUTPUT,
    )
