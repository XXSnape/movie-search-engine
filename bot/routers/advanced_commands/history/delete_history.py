from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendarCallback
from keyboards.inline.callback_factory.history_factory import DeleteHistoryCbData
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from services.history import delete_history_by_date, delete_history_by_interval
from sqlalchemy.ext.asyncio import AsyncSession
from states.history import HistoryFsm
from utils.constants.output_for_user import REQUIRE_ACTION_OUTPUT, SUCCESSFULLY_OUTPUT
from utils.response_formats.pretty_response import get_russian_date
from utils.tg.router_assistants.history import get_calendar

router = Router(name=__name__)


@router.callback_query(HistoryFsm.DELETE, SimpleCalendarCallback.filter())
async def handle_date_for_delete(
    callback: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Удаляет историю по дате

    :param callback: CallbackQuery
    :param callback_data: CallbackData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """
    calendar = await get_calendar(cache=state)
    selected, date = await calendar.process_selection(callback, callback_data)
    if selected:
        await delete_history_by_date(
            session=session, user_id=callback.from_user.id, date=date
        )
        pretty_date = get_russian_date(date)
        await state.clear()
        await callback.answer(
            f"История за {pretty_date} успешно удалена!{SUCCESSFULLY_OUTPUT}",
            show_alert=True,
        )
        await callback.message.answer(
            text=REQUIRE_ACTION_OUTPUT,
            reply_markup=InlineKbForCommand.get_kb_to_select_command(),
        )
        await callback.message.delete()


@router.callback_query(DeleteHistoryCbData.filter())
async def handle_interval_for_delete(
    callback: CallbackQuery,
    callback_data: DeleteHistoryCbData,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Удаляет историю по интервалу

    :param callback: CallbackQuery
    :param callback_data: DeleteHistoryCbData
    :param state: FSMContext
    :param session: сессия для работы с базой
    :return: None
    """

    await delete_history_by_interval(
        session=session,
        user_id=callback.from_user.id,
        cache=state,
        callback_data=callback_data,
    )
    await callback.answer(
        text=f"История успешно удалена!{SUCCESSFULLY_OUTPUT}",
        show_alert=True,
    )
    await callback.message.answer(
        text=REQUIRE_ACTION_OUTPUT,
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )
    await callback.message.delete()
