from abc import ABC
from dataclasses import dataclass


@dataclass
class CacheABC(ABC):
    """
    Абстрактный класс кэша

    text: текст
    photo: картинка
    """

    text: str
    photo: str


@dataclass
class MovieSmallInfoCache(CacheABC):
    """
    Используется для кэширования базовой информации о фильме

    movie_id: id фильма
    """

    movie_id: int


@dataclass
class MovieFromAnotherProjectCache(CacheABC):
    """
    Используется для кэширования информации о связанном фильме

    movie_id: id фильма
    watchability: онлайн-кинотеатры для просмотра
    """

    movie_id: int
    watchability: list[list[str, str]]


@dataclass
class Person(CacheABC):
    """
    Используется для кэширования информации о связанном фильме

    id: id человека

    full_text: информация о человеке. Изначально None.
    Заменяется на текст после запроса пользователя подробной информации

    projects: другие проекты человека. Изначально None.
    Заменяется на id фильмов при запросе подробной информации о человеке.
    Затем id заменяются на MovieFromAnotherProjectCache при запросе информации об этих фильмах
    """

    id: int
    full_text: str | None = None
    projects: list[int | MovieFromAnotherProjectCache] | None = None


@dataclass
class MovieBigInfoCache:
    """
    Используется для кэширования расширенной информации о фильме

    movie_id: id фильма
    title: название фильма
    text: описание фильма
    watchability: онлайн-кинотеатры для просмотра
    actors: актеры
    directors: режисеры
    sequels: продолжения
    similar_projects: похожие фильмы
    """

    movie_id: int
    title: str
    text: str
    watchability: list[list[str, str]]
    actors: list[Person]
    directors: list[Person]
    sequels: list[int | MovieFromAnotherProjectCache]
    similar_projects: list[int | MovieFromAnotherProjectCache]
