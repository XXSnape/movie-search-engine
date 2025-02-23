from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.history_factory import HistoryCbData
from utils.constants.output_for_user import DATE_EXISTS_OUTPUT
from utils.enums.history_data import SelectActionWithHistory
from utils.tg.router_assistants.history import get_calendar_and_max_date

router = Router()


@router.callback_query(
    HistoryCbData.filter(
        F.options.in_(
            (SelectActionWithHistory.VIEW, SelectActionWithHistory.DELETE_BY_DATE)
        )
    ),
)
async def handle_date_selection(
    callback: CallbackQuery, callback_data: HistoryCbData, state: FSMContext
) -> None:
    """
    Обрабатывает выбор даты

    :param callback: CallbackQuery
    :param callback_data: HistoryCbData
    :param state: FSMContext
    :return: None
    """
    calendar, max_date = await get_calendar_and_max_date(
        cache=state, callback_data=callback_data
    )
    await callback.message.edit_text(
        text=f"Пожалуйста, выберете дату со значком {DATE_EXISTS_OUTPUT}",
        reply_markup=await calendar.start_calendar(max_date.year, max_date.month),
    )
