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

    async def get_one_or_none_by_id(self, obj_id: int, session: AsyncSession) -> T | None:
        """Получаем один объект из БД по его ID.

        Args:
            obj_id (int): id объекта
            session (AsyncSession): сессия БД

        Returns:
            T | None: объект или None, если не найден

        """
        try:
            query = select(self.model).filter_by(id=obj_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            logger.info(
                f'Запись {self.model.__name__} с id={obj_id} {"найдена" if result else "не найдена"}.',
            )
            return result
        except SQLAlchemyError as error:
            raise error
