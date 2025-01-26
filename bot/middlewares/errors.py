import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.utils.chat_action import ChatActionSender
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from utils.constants.output_for_user import REQUIRE_ACTION_OUTPUT

logger = logging.getLogger(name=__name__)


class HandleErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        callback: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """
        Обрабатывает любые ошибки при нажатии на кнопку
        :param handler: обработчик
        :param callback: CallbackQuery
        :param data: Dict[str, Any]
        :return: Any
        """
        try:
            async with ChatActionSender.typing(
                bot=callback.bot, chat_id=callback.from_user.id
            ):
                result = await handler(callback, data)
                return result
        except Exception:
            await callback.answer("Сделайте запрос снова", show_alert=True)
            await callback.message.answer(
                REQUIRE_ACTION_OUTPUT,
                reply_markup=InlineKbForCommand.get_kb_to_select_command(),
            )
            try:
                await callback.message.delete()
            except TelegramBadRequest:
                logger.exception("Произошла ошибка при удалении callback")
            logger.exception("Произошла ошибка в callback")
