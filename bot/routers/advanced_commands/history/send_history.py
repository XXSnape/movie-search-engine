from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession
from states.history import HistoryFsm
from utils.tg.router_assistants.history import (
    get_calendar,
    send_first_movie_from_history,
)

router = Router()


@router.callback_query(HistoryFsm.VIEW, SimpleCalendarCallback.filter())
async def handle_sending_history(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CallbackData,
    session: AsyncSession,
) -> None:
    """
    Отправляет фильм из истории

    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: CallbackData
    :param session: сессия для работы с базой
    :return: None
    """
    calendar = await get_calendar(cache=state)
    selected, date = await calendar.process_selection(callback, callback_data)
    if selected:
        await send_first_movie_from_history(
            session=session,
            callback=callback,
            cache=state,
            date=date,
            calendar=calendar,
        )
