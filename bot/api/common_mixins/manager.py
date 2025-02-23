import logging

import aiohttp
from config.settings import settings

logger = logging.getLogger(__name__)


class ManagerAPIMixin:
    """
    Миксин-класс для работы с api kinopoisk

    BASE_URL: базовый url для всех запросов
    HEADERS: необходимые заголовки для запросов
    additional_url: дополнительный url, добавляющийся к базовому
    """

    BASE_URL = "https://api.kinopoisk.dev/v1.4/"  #
    HEADERS = {"X-API-KEY": settings.API.API_KEY}
    additional_url = ""

    @classmethod
    async def _make_request(
        cls,
        url: str | int = "",
        params: dict | None = None,
    ) -> dict | None:
        """
        Делает запрос

        :param url: название ресурса, на который нужно сделать запрос
        :param params: дополнительные параметры запроса
        :return: словарь или None, если произойдет ошибка
        """
        if url != "":
            url = f"/{url}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"{cls.BASE_URL}{cls.additional_url}{url}",
                    params=params,
                    headers=cls.HEADERS,
                    timeout=10,
                ) as response:
                    logger.info("params = %s", params)
                    if response.status != 200:
                        logger.error(
                            "status incorrect: %s %s",
                            response.status,
                            await response.text(),
                        )
                        return None
                    return await response.json()
        except Exception:
            logger.exception("Произошла ошибка при запросе")
            return None

    @classmethod
    def _validate_response(cls, data: dict) -> bool:
        """
        Проверяет ответ от api на наличие каких-либо данных

        :param data: словарь с данными
        :return: True, если данные есть, иначе False
        """
        return len(data["docs"]) != 0
