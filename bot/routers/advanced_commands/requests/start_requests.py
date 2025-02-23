from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from utils.enums.commands import Commands
from utils.tg.router_assistants.request import handle_requests

router = Router(name=__name__)


@router.callback_query(F.data == Commands.REQUESTS)
async def handle_start_requests(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабатывает команду REQUESTS

    :param callback: CallbackQuery
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    await handle_requests(
        session=session,
        callback=callback,
        cache=state,
    )
