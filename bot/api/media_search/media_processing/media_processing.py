from aiogram.types import InputMediaPhoto
from api.media_search.media_from_api.media_data import MediaDataApi


def get_pictures(json: dict) -> list[InputMediaPhoto]:
    """
    Конвертирует url картинок в телеграм-объекты
    :param json: данные из api
    :return: список из InputMediaPhoto
    """
    return [InputMediaPhoto(media=url) for url in MediaDataApi.get_pictures(json)]
