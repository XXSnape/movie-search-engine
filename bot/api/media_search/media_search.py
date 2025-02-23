from aiogram.types import InputMediaPhoto
from config.settings import settings

from .media_mixins import MediaApiMixin
from .media_processing import get_pictures


class MediaSearch(MediaApiMixin):
    """
    Класс для отправки запросов на api
    """

    @classmethod
    async def get_photos_by_id(cls, movie_id: int) -> list[InputMediaPhoto]:
        """
        Получает картинки фильма по его id

        :param movie_id: id фильма
        :return: список с InputMediaPhoto
        """
        params = {
            "page": 1,
            "limit": settings.API.NUMBER_PHOTOS,
            "selectFields": ["previewUrl"],
            "notNullFields": ["previewUrl"],
            "movieId": [movie_id],
        }
        json_resp = await cls._make_request(params=params)
        return get_pictures(json_resp)
