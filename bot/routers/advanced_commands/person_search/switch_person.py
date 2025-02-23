from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import PersonSearch
from keyboards.inline import InlineKbForPerson
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.process_photo import edit_photo

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(
        F.options.in_((ViewingMovieDetails.ACTORS, ViewingMovieDetails.DIRECTORS))
    )
)
async def handle_next_or_prev_person(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Переключает людей

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    person, title, length = await PersonSearch.get_person_title_and_len(
        callback_data=callback_data,
        cache=state,
    )
    markup = InlineKbForPerson.get_kb_to_switch_persons_and_view_details(
        data_for_back=callback_data, title=title, length=length
    )
    await edit_photo(
        callback=callback, text=person.text, photo=person.photo, markup=markup
    )
