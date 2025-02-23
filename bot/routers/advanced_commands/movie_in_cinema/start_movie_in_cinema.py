from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.constants.api_data import YEAR_SORT
from utils.constants.cache_keys import PARAMS_CACHE
from utils.constants.output_for_user import GENRE_OUTPUT
from utils.enums.commands import Commands
from utils.tg.router_assistants.survey import go_to_selection_items

router = Router(name=__name__)


@router.callback_query(F.data == Commands.MOVIE_IN_CINEMA)
async def handle_genres_of_movie(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду MOVIE_IN_CINEMA. Предоставляет выбор жанров
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await callback.message.delete()
    await state.update_data({PARAMS_CACHE: {"ticketsOnSale": ["true"]}})
    await go_to_selection_items(
        message=callback.message,
        cache=state,
        data_fsm=SearchMovieByDataFSM.genres,
        command=Commands.MOVIE_IN_CINEMA,
        text=GENRE_OUTPUT,
        sort_field=YEAR_SORT,
    )
