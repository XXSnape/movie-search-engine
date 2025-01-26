from logging import getLogger

from database.core.db_helper import db_helper
from database.repository.request import RequestRepository

logger = getLogger(__name__)


async def delete_requests_by_time() -> None:
    """
    Удаляет запросы пользователей
    """
    session = await db_helper.get_async_session()
    try:
        logger.info("Начинается удаление запросов пользователей")
        await RequestRepository.delete_requests(session=session)
        logger.info("Удаление запросов успешно завершено")
    except Exception:
        logger.exception("Не удалось удалить запросы")
    await session.close()
