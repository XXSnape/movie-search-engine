from api.common_mixins import ManagerAPIMixin


class ReviewApiMixin(ManagerAPIMixin):
    """
    Класс-миксин для работы с отзывами
    """

    additional_url = "review"
