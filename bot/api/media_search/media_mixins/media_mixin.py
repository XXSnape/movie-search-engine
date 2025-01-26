from api.common_mixins import ManagerAPIMixin


class MediaApiMixin(ManagerAPIMixin):
    """
    Класс-миксин для работы с медиа
    """

    additional_url = "image"
