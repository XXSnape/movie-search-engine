import logging
from typing import Any, Sequence

from database.repository.abstract_repositories import AbstractRepository
from sqlalchemy import Row, RowMapping, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(name=__name__)


class ManagerRepository(AbstractRepository):
    """
    Класс - репозиторий, реализующий все методы абстрактного класса.
    """

    model = None  # Модель базы данных

    @classmethod
    async def create_object(
        cls,
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
        stmt = insert(cls.model).values(**data).returning(cls.model.id)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

        except IntegrityError as err:
            await session.rollback()
            if "foreign key constraint" in err.args[0]:
                return False

    @classmethod
    async def delete_object_by_params(
        cls,
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
        stmt = delete(cls.model).filter_by(**data).returning(cls.model.id)
        result = await session.execute(stmt)
        result = bool(result.fetchone())
        await session.commit()
        return result

    @classmethod
    async def get_objects_by_params(
        cls, session: AsyncSession, data: dict
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        Ищет объект в базе данных.

        Параметры:

        session: Сессия для асинхронной работы с базой данных
        data: Словарь с данными, по которым будет осуществлен поиск объекта

        Возвращает объект базы данных или None.
        """
        query = select(cls.model).filter_by(**data)
        result = await session.execute(query)
        return result.scalars().all()

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
        stmt = update(cls.model).filter_by(**filter_data).values(**update_data)
        await session.execute(stmt)
        await session.commit()
