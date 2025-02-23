from enum import IntEnum, auto


class ViewingMovieDetails(IntEnum):
    """
    MOVIES - просмотр базовой информации о фильмах
    MOVIE_DETAILS - просмотр деталей фильма
    WATCH - онлайн-кинотеатры
    PICTURES - картинки фильма
    ACTORS - актеры в фильме
    DIRECTORS - режиссеры фильма
    ACTOR_DETAILS - дополнительная информация об актерах
    DIRECTOR_DETAILS - дополнительная информация о режиссерах
    SEQUELS - продолжения
    SIMILAR_PROJECTS - похожие кино-проекты
    ACTOR_PROJECTS - другие проекты актеров фильма
    DIRECTOR_PROJECTS - другие проекты режиссеров фильма
    SELECT_REVIEWS - выбор типов отзывов
    VIEWING_REVIEWS - просмотр отзывов

    DOWNLOAD_FOLLOWING - загрузить следующую страницу в api
    DOWNLOAD_PREVIOUS - загрузить предыдущую страницу в api
    """

    MOVIES = auto()
    MOVIE_DETAILS = auto()
    WATCH = auto()
    PICTURES = auto()
    ACTORS = auto()
    DIRECTORS = auto()
    ACTOR_DETAILS = auto()
    DIRECTOR_DETAILS = auto()
    SEQUELS = auto()
    SIMILAR_PROJECTS = auto()
    ACTOR_PROJECTS = auto()
    DIRECTOR_PROJECTS = auto()
    SELECT_REVIEWS = auto()
    VIEWING_REVIEWS = auto()

    DOWNLOAD_FOLLOWING = auto()
    DOWNLOAD_PREVIOUS = auto()
