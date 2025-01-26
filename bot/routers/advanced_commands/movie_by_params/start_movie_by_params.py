from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config.settings import settings
from keyboards.inline import InlineKbForSurvey
from states.movie_search import SearchMovieByDataFSM
from utils.constants.api_data import PREMIERE_SORT, RATING_SORT, YEAR_SORT
from utils.constants.cache_keys import PARAMS_CACHE
from utils.constants.output_for_user import NETWORK_OUTPUT
from utils.enums.commands import Commands
from utils.enums.items import SortItem, SortType
from utils.response_formats.texts import SELECT_SORTING
from utils.tg.router_assistants.survey import go_to_selection_items

router = Router(name=__name__)


@router.callback_query(F.data == Commands.MOVIE_BY_PARAMS)
async def handle_sorting_selection(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду MOVIE_BY_PARAMS. Предоставляет выбор типа сортировки
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await state.set_state(SearchMovieByDataFSM.sorting)
    await callback.message.edit_text(
        text=SELECT_SORTING,
        reply_markup=InlineKbForSurvey.get_buttons_to_select_sort_type(),
    )


@router.callback_query(SearchMovieByDataFSM.sorting)
async def handle_networks_of_movie(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Предоставляет выбор сети производителя фильмов
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    if callback.data == str(SortType.BY_YEAR):
        await state.update_data(
            {
                PARAMS_CACHE: {
                    "page": 1,
                    "limit": settings.API.NUMBER_FILMS,
                    "sortField": [YEAR_SORT, PREMIERE_SORT, RATING_SORT],
                    "sortType": [SortItem.DESCEND, SortItem.DESCEND, SortItem.DESCEND],
                }
            }
        )
    await callback.message.delete()
    await go_to_selection_items(
        message=callback.message,
        cache=state,
        data_fsm=SearchMovieByDataFSM.networks,
        command=Commands.MOVIE_BY_PARAMS,
        text=NETWORK_OUTPUT,
        combine_selection=False,
        change_cache=callback.data != str(SortType.BY_YEAR),
    )
