from api.common_mixins import ManagerAPIMixin


class MovieApiMixin(ManagerAPIMixin):
    """
    Класс-миксин для работы с фильмами
    """

    additional_url = "movie"
