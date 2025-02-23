from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from keyboards.inline.keyboards.survey_kb import InlineKbForSurvey
from states.movie_search import SearchMovieByDataFSM
from utils.buttons.get_buttons import get_buttons_for_back_by_callback
from utils.constants.cache_keys import BUTTONS_CACHE, CALLBACK_DATA_CACHE
from utils.constants.router_keys import END_ROUTER
from utils.enums.movie_data import ViewingMovieDetails
from utils.response_formats import get_text_for_survey
from utils.tg.router_assistants.review import send_first_review

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(F.options == ViewingMovieDetails.SELECT_REVIEWS)
)
async def handle_selection_of_types(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Обрабатывает выбор типов отзывов

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    buttons_for_back = await get_buttons_for_back_by_callback(callback_data, state)
    markup, buttons = InlineKbForSurvey.get_kb_to_select_buttons(
        SearchMovieByDataFSM.reviews, buttons_for_back
    )
    await state.set_state(SearchMovieByDataFSM.reviews)
    await state.update_data(
        {CALLBACK_DATA_CACHE: callback_data, BUTTONS_CACHE: buttons}
    )
    await callback.message.edit_text(
        text=get_text_for_survey("тип интересующих отзывов", combine_selection=False),
        reply_markup=markup,
    )


@router.callback_query(SearchMovieByDataFSM.reviews, F.data == END_ROUTER)
async def handle_types_reviews_and_send_review(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает типы отзывов и отправляет отзыв
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await send_first_review(callback=callback, cache=state)
