import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.settings import configure_logging, settings
from middlewares.errors import HandleErrorMiddleware
from routers import router as main_router
from utils.scheduler.tasks import delete_requests_by_time


async def main() -> None:
    """
    Функция для запуска бота и задач по расписанию

    :return: None
    """
    configure_logging()
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone="Europe/Moscow")
    scheduler.add_job(
        delete_requests_by_time,
        "cron",
        hour="0",
        minute="0",
    )
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(HandleErrorMiddleware())
    bot = Bot(
        token=settings.TG.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
