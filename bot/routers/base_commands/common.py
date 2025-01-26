from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from utils.constants.commands import COMMANDS_AND_DESCRIPTIONS
from utils.constants.output_for_user import (
    GUARANTEED_ELEMENT,
    REQUIRE_ACTION_OUTPUT,
    SUCCESSFULLY_OUTPUT,
)
from utils.constants.router_keys import CANCEL_ROUTER
from utils.response_formats import build_text

router = Router()


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    """
    Обрабатывает команду help
    :param message: Message
    :return: None
    """
    commands = "\n".join(
        f"Команда {build_text(command)} - {description}\n"
        for command, description in COMMANDS_AND_DESCRIPTIONS
    )
    await message.answer(
        text=f"Доступные команды:\n\n{commands}\n\n"
        "При прохождении опроса можно выбрать несколько вариантов ответа или ни одного.\n\n"
        f"Если рядом с элементом значок {SUCCESSFULLY_OUTPUT}, и другой элемент с таким же значком, то в ответ попадет этот элемент или другой, или вместе.\n\n"
        f"Если же с элементами значок {GUARANTEED_ELEMENT}, то эти элементы будут гарантированно вместе.\n\n"
        "Пример 1:\n\n"
        f"Россия{SUCCESSFULLY_OUTPUT}\n"
        f"Китай{SUCCESSFULLY_OUTPUT}\n"
        "\n\n"
        "Значит попадут в выборку российские или китайские фильмы"
        "\n\n"
        "Пример 2:\n\n"
        f"Драма{GUARANTEED_ELEMENT}\n"
        f"Комедия{GUARANTEED_ELEMENT}\n\n"
        "В этом случае бот покажет только фильмы, которые являются и комедиями, и драмами.",
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )


@router.callback_query(F.data == CANCEL_ROUTER)
async def handle_end(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает отмену действий. Сбрасывает все состояние.

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        text=REQUIRE_ACTION_OUTPUT,
        reply_markup=InlineKbForCommand.get_kb_to_select_command(),
    )
