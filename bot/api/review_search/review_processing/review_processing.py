from api.review_search.review_from_api import ReviewDataApi
from utils.response_formats import present_data


def get_text_review(json: dict) -> str:
    """
    Получает текст о человеке

    :param json: данные из api
    :return: текст о человеке
    """
    return present_data(ReviewDataApi.get_review(json))
