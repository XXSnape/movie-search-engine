from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config.settings import settings
from keyboards.inline import InlineKbForSurvey
from keyboards.inline.callback_factory.survey_factory import CollectionCbData
from states.movie_search import SearchMovieByDataFSM
from utils.constants.api_data import COLLECTION_KEY, YEAR_SORT
from utils.constants.cache_keys import COMMAND_CACHE, MIN_PAGE_CACHE, PARAMS_CACHE
from utils.constants.output_for_user import ONLINE_CINEMA_OUTPUT
from utils.enums.commands import Commands
from utils.enums.items import SortItem
from utils.tg.router_assistants.survey import move_to_new_stage

router = Router(name=__name__)


@router.callback_query(CollectionCbData.filter())
async def handle_category_and_send_collection(
    callback: CallbackQuery, callback_data: CollectionCbData, state: FSMContext
) -> None:
    """
    Обрабатывает категории и отправляет коллекции на выбор

    :param callback: CallbackQuery
    :param callback_data: CollectionCbData
    :param state: FSMContext
    :return: None
    """
    markup = InlineKbForSurvey.get_kb_to_select_collection(callback_data)
    await state.set_state(SearchMovieByDataFSM.collection)
    await callback.message.edit_text(
        text="Выберете интересующую коллекцию", reply_markup=markup
    )


@router.callback_query(SearchMovieByDataFSM.collection)
async def handle_collection_and_send_cinemas(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает коллекцию и отправляет фильм

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    params = {
        "page": 1,
        "limit": settings.API.NUMBER_FILMS,
        "sortField": YEAR_SORT,
        "sortType": [SortItem.DESCEND],
        COLLECTION_KEY: [f"+{callback.data}"],
    }
    await state.update_data(
        {
            PARAMS_CACHE: params,
            MIN_PAGE_CACHE: 1,
            COMMAND_CACHE: Commands.MOVIE_BY_COLLECTIONS,
        }
    )
    await move_to_new_stage(
        callback, state, SearchMovieByDataFSM.collection_cinemas, ONLINE_CINEMA_OUTPUT
    )
