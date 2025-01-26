from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.inline.keyboards.command_kb import InlineKbForCommand

router = Router(name=__name__)


@router.message()
async def handle_unrecognized_message(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает нераспознанное сообщение и сбрасывает состояние
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await message.reply(
        text="Сообщение не распознано, пожалуйста, введите /help",
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )
