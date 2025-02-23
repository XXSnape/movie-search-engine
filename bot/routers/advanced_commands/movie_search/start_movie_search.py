from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from states.movie_search import SearchMovieByTitleFSM
from utils.enums.commands import Commands

router = Router(name=__name__)


@router.callback_query(F.data == Commands.MOVIE_SEARCH)
async def handle_movie_search(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду MOVIE_SEARCH

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await callback.message.delete()
    await state.set_state(SearchMovieByTitleFSM.title)
    await callback.message.answer(
        text="Напишите название интересующего произведения киноиндустрии",
        reply_markup=InlineKbForCommand.get_kb_to_exit_command(),
    )
