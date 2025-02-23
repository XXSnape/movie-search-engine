from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_data_from_cache
from keyboards.inline import InlineKbForSurvey
from keyboards.inline.callback_factory.survey_factory import MovieCbData
from states.movie_search import SearchMovieByDataFSM
from utils.constants.cache_keys import BUTTONS_CACHE

router = Router(name=__name__)


@router.callback_query(
    StateFilter(
        SearchMovieByDataFSM.genres,
        SearchMovieByDataFSM.types,
        SearchMovieByDataFSM.countries,
        SearchMovieByDataFSM.statuses,
        SearchMovieByDataFSM.cinemas,
        SearchMovieByDataFSM.reviews,
        SearchMovieByDataFSM.networks,
        SearchMovieByDataFSM.collection_cinemas,
    ),
    MovieCbData.filter(),
)
async def handle_user_clicks_when_selecting(
    callback: CallbackQuery, callback_data: MovieCbData, state: FSMContext
) -> None:
    """
    Обрабатывает пользовательский выбор. Изменяет нажатую кнопку

    :param callback: CallbackQuery
    :param callback_data: MovieCbData
    :param state: FSMContext
    :return: None
    """
    buttons = await get_data_from_cache(BUTTONS_CACHE, cache=state)
    markup = await InlineKbForSurvey.get_kb_with_modified_btn(
        callback_data, buttons, state
    )
    await callback.message.edit_reply_markup(reply_markup=markup)
