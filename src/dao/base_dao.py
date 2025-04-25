from typing import Generic, Type, TypeVar

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from core.base_model import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    """Базовый класс для всех DAO."""

    model: Type[T] = None

    def __init__(self) -> None:  # noqa: D107
        if self.model is None:
            raise ValueError('Модель должна быть указана в дочернем классе')

    async def get_one_or_none_by_id(self, session: AsyncSession, obj_id: int) -> T | None:
        """Получаем один объект из БД по его ID.

        Args:
            obj_id (int): id объекта
            session (AsyncSession): сессия БД

        Returns:
            T | None: объект или None, если не найден

        """
        try:
            logger.info(f'Ищем запись {self.model.__name__} с id={obj_id}')
            query = select(self.model).filter_by(id=obj_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            logger.info(
                f'Запись {self.model.__name__} с id={obj_id} {"найдена" if result else "не найдена"}.',
            )
            return result
        except SQLAlchemyError as error:
            logger.error(f'Ошибка при поиске записи с ID {obj_id}: {error}')
            raise error

    async def find_one_or_none(self, session: AsyncSession, filter_params: dict | None = None) -> T | None:
        """Поиск одной записи по параметрам.

        Args:
            session (AsyncSession): сессия БД
            filter_params (dict): параметры для поиска

        Returns:
            T | None: найденная запись или None, если не найдена

        """
        try:
            if not filter_params:
                filter_params = {}
            logger.info(f'Ищем запись {self.model.__name__} по параметрам {filter_params}')
            query = select(self.model).filter_by(**filter_params)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            logger.info(
                f'Запись {self.model.__name__} с по параметрами {filter_params} '
                f'{"найдена" if result else "не найдена"}.',
            )

            return result

        except SQLAlchemyError as error:
            logger.error(f'Ошибка при поиске записи по параметрам {filter_params}: {error}')
            raise error

    async def find_all(self, session: AsyncSession, filter_params: dict | None = None) -> list[T] | None:
        """Поиск одной записи по параметрам.

        Args:
            session (AsyncSession): сессия БД
            filter_params (dict): параметры для поиска

        Returns:
            list[T] | None: найденные записи или None, если не найдено

        """
        try:
            if not filter_params:
                filter_params = {}
            logger.info(f'Ищем записи {self.model.__name__} по параметрам {filter_params}')
            query = select(self.model).filter_by(**filter_params)
            result = await session.execute(query)
            result = result.scalars().all()
            logger.info(
                f'Найдено {len(result)} записей {self.model.__name__} с по параметрами {filter_params} ',
            )

            return result if result else None

        except SQLAlchemyError as error:
            logger.error(f'Ошибка при поиске записей по параметрам {filter_params}: {error}')
            raise error
