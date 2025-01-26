from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.core.db_helper import db_helper


class DbSessionMiddleware(BaseMiddleware):
    """
    Создает сессию для работы с базой
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        По ключу "session" добавляет сессию

        :param handler: обработчик
        :param event: TelegramObject
        :param data: Dict[str, Any]
        :return: Any
        """
        async_session = await db_helper.get_async_session()
        data["session"] = async_session
        result = await handler(event, data)
        await async_session.close()
        data.pop("session")
        return result
