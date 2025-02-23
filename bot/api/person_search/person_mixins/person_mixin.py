from api.common_mixins import ManagerAPIMixin


class PersonApiMixin(ManagerAPIMixin):
    """
    Класс-миксин для работы с людьми
    """

    additional_url = "person"
