"""
Модуль с абстрактными репозиториями для работы с таблицами базы данных.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """
    Абстрактный класс - репозиторий.
    """

    @abstractmethod
    async def create_object(
        self,
        session: AsyncSession,
        data: dict,
    ) -> int:
        """
        Добавляет новый объект в базу данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, которые должны быть добавлены в базу

        Возвращает идентификатор добавленной записи.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_object_by_params(
        self,
        session: AsyncSession,
        data: dict,
    ) -> bool:
        """
        Удаляет объекты из базы данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объектов для удаления

        Возвращает True, если объекты были удалены и False в противном случае.
        """
        raise NotImplementedError

    @classmethod
    async def update_object_by_params(
        cls, session: AsyncSession, filter_data: dict, update_data: dict
    ) -> None:
        """
        Обновляет объекты по параметрам.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        filter_data: Словарь с данными для фильтрации
        update_data: Словарь с данными для обновления

        Возвращает None
        """
        raise NotImplementedError

    @classmethod
    async def get_objects_by_params(
        cls, session: AsyncSession, data: dict
    ) -> Optional[Any]:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает объект базы данных или None.
        """
        raise NotImplementedError
