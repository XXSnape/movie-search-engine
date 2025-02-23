import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TGSettings(BaseSettings):
    """
    Класс с настройками работы телеграма
    """

    BOT_TOKEN: str


class APISettings(BaseSettings):
    """
    Класс с настройками работы api
    """

    API_KEY: str
    NUMBER_FILMS: int
    NUMBER_REVIEWS: int
    NUMBER_PHOTOS: int
    NUMBER_PERSONS: int
    NUMBER_PROJECTS: int
    DAYS_BEFORE_DELETION: int


class DBSettings(BaseSettings):
    """
    Класс для настройки параметров подключения к базе данных.
    """

    HOST: str
    PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    echo: bool = False

    @property
    def database_url(self) -> str:
        """
        Возвращает строку для подключения к базе данных.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.POSTGRES_DB}"
        )


class Settings(BaseSettings):
    """
    Класс с настройками телеграма, api и базы данных
    """

    TG: TGSettings = TGSettings()
    API: APISettings = APISettings()
    DB: DBSettings = DBSettings()


def configure_logging(level=logging.INFO) -> None:
    """
    Конфигурирует настройки логирования

    :param level: Уровень логирования
    :return: None
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


settings = Settings()
