from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.movie_search import SearchMovieByDataFSM
from utils.constants.output_for_user import STATUS_OUTPUT
from utils.enums.commands import Commands
from utils.tg.router_assistants.survey import go_to_selection_items

router = Router(name=__name__)


@router.callback_query(F.data == Commands.MOVIE_BY_STATUSES)
async def handle_statuses_of_movie(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду MOVIE_BY_STATUSES
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await callback.message.delete()
    await go_to_selection_items(
        message=callback.message,
        cache=state,
        data_fsm=SearchMovieByDataFSM.statuses,
        command=Commands.MOVIE_BY_STATUSES,
        text=STATUS_OUTPUT,
        combine_selection=False,
    )
