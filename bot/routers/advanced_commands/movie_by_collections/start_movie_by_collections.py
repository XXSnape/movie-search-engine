from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils.enums.commands import Commands
from utils.tg.router_assistants.movie import handle_collections

router = Router(name=__name__)


@router.callback_query(F.data == Commands.MOVIE_BY_COLLECTIONS)
async def handle_type_of_collections(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает команду MOVIE_BY_COLLECTIONS

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await callback.message.delete()
    await callback.answer()
    await handle_collections(message=callback.message, cache=state)
