from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import PersonSearch
from keyboards.inline import InlineKbForPerson
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.enums.movie_data import ViewingMovieDetails

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(
        F.options.in_(
            (
                ViewingMovieDetails.ACTOR_DETAILS,
                ViewingMovieDetails.DIRECTOR_DETAILS,
            )
        )
    )
)
async def handle_details_person(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Обрабатывает детальную информацию о человеке

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    person, title = await PersonSearch.get_detail_person_and_title(
        callback_data=callback_data, cache=state
    )
    await callback.message.edit_caption(
        caption=person.full_text,
        reply_markup=InlineKbForPerson.get_kb_for_back_to_persons_and_view_other_projects(
            callback_data, person.projects, title
        ),
    )
