class MediaDataApi:
    """
    Класс с функциями, связанными с картинками, достающими данные из ответа api
    """

    @classmethod
    def get_pictures(cls, json: dict) -> list[str]:
        """
        Получает url картинок из json

        :param json: данные от api
        :return: список с картинками
        """
        return [preview["previewUrl"] for preview in json["docs"]]
