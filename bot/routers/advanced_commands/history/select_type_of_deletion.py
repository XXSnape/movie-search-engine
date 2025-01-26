from aiogram import F, Router
from aiogram.types import CallbackQuery
from keyboards.inline.callback_factory.history_factory import HistoryCbData
from keyboards.inline.keyboards.history_kb import InlineKbForHistory
from utils.enums.history_data import SelectActionWithHistory

router = Router()


@router.callback_query(
    HistoryCbData.filter(F.options == SelectActionWithHistory.DELETE)
)
async def handle_options_for_deleting(callback: CallbackQuery) -> None:
    """
    Обрабатывает период для удаления
    :param callback: CallbackQuery
    :return: None
    """
    markup = InlineKbForHistory.get_kb_to_select_delete_options()
    await callback.message.edit_text(
        "За какое время удалить историю?", reply_markup=markup
    )
