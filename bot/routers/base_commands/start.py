from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline.keyboards.command_kb import InlineKbForCommand

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """
    Обрабатывает команду start
    :param message: Message
    :return: None
    """
    await message.answer(
        text=f"Добрый день, {message.from_user.full_name}!\n\n"
        "Я бот, который поможет найти то,"
        " что вы хотите посмотреть легко и удобно без регистрации.\n\n"
        "Для дополнительной информации введите /help",
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )
