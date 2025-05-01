from typing import Generic, Type, TypeVar

from loguru import logger
from pydantic import BaseModel
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

    async def get_one_or_none_by_id(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> T | None:
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

    async def find_one_or_none(
        self,
        session: AsyncSession,
        filter_params: dict | None = None,
    ) -> T | None:
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
            logger.info(
                f'Ищем запись {self.model.__name__} по параметрам {filter_params}',
            )
            query = select(self.model).filter_by(**filter_params)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            logger.info(
                f'Запись {self.model.__name__} с по параметрами {filter_params} '
                f'{"найдена" if result else "не найдена"}.',
            )

            return result

        except SQLAlchemyError as error:
            logger.error(
                f'Ошибка при поиске записи по параметрам {filter_params}: {error}',
            )
            raise error

    async def find_all(
        self,
        session: AsyncSession,
        filter_params: dict | None = None,
    ) -> list[T] | None:
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
            logger.info(
                f'Ищем записи {self.model.__name__} по параметрам {filter_params}',
            )
            query = select(self.model).filter_by(**filter_params)
            result = await session.execute(query)
            result = result.scalars().all()
            logger.info(
                f'Найдено {len(result)} записей {self.model.__name__} с параметрами {filter_params} ',
            )

            return result if result else None

        except SQLAlchemyError as error:
            logger.error(
                f'Ошибка при поиске записей по параметрам {filter_params}: {error}',
            )
            raise error

    async def create(self, session: AsyncSession, new_object: BaseModel) -> T:
        """Создаем новый объект в БД.

        Args:
            session (AsyncSession): сессия БД
            new_object (BaseModel): данные объекта для создания

        Returns:
            T: созданный объект

        """
        try:
            object_data = new_object.model_dump(exclude_unset=True)
            logger.info(f'Создаем запись {self.model.__name__} с данными {object_data}')
            new_instance = self.model(**object_data)
            session.add(new_instance)
            await session.commit()
            await session.refresh(new_instance)
            logger.info(
                f'Запись {self.model.__name__} с данными {object_data} создана.',
            )
            return new_instance
        except SQLAlchemyError as error:
            logger.error(
                f'Ошибка при создании записи {self.model.__name__} с данными {object_data}: {error}',
            )
            raise error

    async def update(
        self,
        session: AsyncSession,
        update_object: T,
        update_data: BaseModel,
    ) -> T:
        """Обновляем объект в БД.

        Args:
            session (AsyncSession): сессия БД
            update_object (T): объект для обновления
            update_data (BaseModel): данные для обновления

        Returns:
            T: обновленный объект

        """
        try:
            object_data = update_data.model_dump(exclude_unset=True)
            logger.info(
                f'Обновляем запись {self.model.__name__} с данными {object_data}',
            )
            for key, value in object_data.items():
                if hasattr(update_object, key):
                    setattr(update_object, key, value)
            session.add(update_object)
            await session.commit()
            await session.refresh(update_object)
            logger.info(
                f'Запись {self.model.__name__} с данными {object_data} обновлена.',
            )
            return update_object
        except SQLAlchemyError as error:
            logger.error(
                f'Ошибка при обновлении записи {self.model.__name__} с данными {object_data}: {error}',
            )
            raise error

    async def delete(self, session: AsyncSession, delete_object: T) -> None:
        """Удаляем объект из БД.

        Args:
            session (AsyncSession): сессия БД
            delete_object (T): объект для удаления

        Returns:
            None

        """
        try:
            logger.info(f'Удаляем запись {self.model.__name__} с ID {delete_object.id}')
            await session.delete(delete_object)
            await session.commit()
            logger.info(
                f'Запись {self.model.__name__} с ID {delete_object.id} удалена.',
            )
        except SQLAlchemyError as error:
            logger.error(
                f'Ошибка при удалении записи {self.model.__name__} с ID {delete_object.id}: {error}',
            )
            raise error
