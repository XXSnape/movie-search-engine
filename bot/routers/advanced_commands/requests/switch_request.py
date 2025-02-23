from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from cache.get_data import get_request_and_len
from keyboards.inline.callback_factory.request_factory import RequestCbData
from keyboards.inline.keyboards.request_kb import InlineKbForRequest
from utils.enums.request_data import SelectActionWithRequest

router = Router(name=__name__)


@router.callback_query(
    RequestCbData.filter(F.options == SelectActionWithRequest.SWITCH)
)
async def handle_next_or_prev_request(
    callback: CallbackQuery,
    callback_data: RequestCbData,
    state: FSMContext,
) -> None:
    """
    Переключает запросы
    :param callback: CallbackQuery
    :param callback_data: RequestCbData
    :param state: FSMContext
    :return: None
    """
    request, length = await get_request_and_len(idx=callback_data.index, cache=state)
    markup = InlineKbForRequest.get_kb_to_select_actions(
        idx=callback_data.index, length=length
    )
    await callback.message.edit_text(text=request.text, reply_markup=markup)
