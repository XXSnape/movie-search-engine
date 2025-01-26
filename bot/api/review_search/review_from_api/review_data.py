from utils.response_formats import get_pretty_date


class ReviewDataApi:
    """
    Класс с функциями, связанными с отзывами, достающими данные из ответа api
    """

    @classmethod
    def get_review(cls, json: dict) -> dict[str, str]:
        """
        Получает отзыв
        :param json: данные из апи
        :return: словарь в читаемом виде
        """
        return {
            "Заголовок": json.get("title"),
            "Тип": json.get("type"),
            "Отзыв": json.get("review"),
            "Дата": get_pretty_date(json.get("date")),
            "Автор": json.get("author"),
        }
