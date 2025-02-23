from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.button_cache import fill_in_params_on_buttons
from keyboards.reply.survey_kb import ReplyKbForSurvey
from states.movie_search import SearchMovieByDataFSM
from utils.buttons import ParseDataFromCb
from utils.constants.api_data import COUNTRY_KEY
from utils.constants.router_keys import END_ROUTER
from utils.response_formats import TEXT_OVER_YEARS
from utils.survey_data import RUSSIAN_COUNTRIES

router = Router()


@router.callback_query(SearchMovieByDataFSM.countries, F.data == END_ROUTER)
async def handle_countries_and_send_years_of_creation_movie(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает страны и отправляет годы на выбор
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await fill_in_params_on_buttons(
        cache=state,
        key=COUNTRY_KEY,
        get_cb=ParseDataFromCb(storage=RUSSIAN_COUNTRIES),
    )
    markup = ReplyKbForSurvey.get_kb_for_select_years()
    msg = callback.message
    await state.set_state(SearchMovieByDataFSM.years)
    await callback.message.delete()
    await msg.answer(TEXT_OVER_YEARS, reply_markup=markup)
