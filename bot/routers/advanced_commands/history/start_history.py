from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.commands import Commands
from utils.tg.router_assistants.history import handle_history

router = Router(name=__name__)


@router.callback_query(F.data == Commands.HISTORY)
async def handle_start_history(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает команду HISTORY
    :param callback: CallbackQuery
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    await handle_history(
        session=session,
        callback=callback,
        cache=state,
    )
