import contextlib
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    """Управление сессиями и соединениями с БД."""

    def __init__(self) -> None:  # noqa: D107
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, db_url: str) -> None:
        """Инициализация соединения с БД.

        Args:
            db_url (str): URL соединения с БД.

        """
        if 'postgresql' in db_url:
            connect_args = {
                'statement_cache_size': 0,
                'prepared_statement_cache_size': 0,
            }
        else:
            connect_args = {}
        self._engine = create_async_engine(
            url=db_url,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        """Закрытие соединения с БД."""
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session_without_commit(self) -> AsyncIterator[AsyncSession]:
        """Получение сессии работы с БД без коммита."""
        if self._sessionmaker is None:
            raise IOError('DatabaseSessionManager is not initialized')
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @contextlib.asynccontextmanager
    async def session_with_commit(self) -> AsyncIterator[AsyncSession]:
        """Получение сессии работы с БД с коммитом."""
        if self._sessionmaker is None:
            raise IOError('DatabaseSessionManager is not initialized')
        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Получение соединения с БД."""
        if self._engine is None:
            raise IOError('DatabaseSessionManager is not initialized')
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()


async def get_session_without_commit() -> AsyncIterator[AsyncSession]:
    """Получение сессии для зависимостей FastAPI без комита."""
    # This is Fastapi dependency
    # session: AsyncSession = Depends(get_session)
    async with db_manager.session_without_commit() as session:
        yield session


async def get_session_with_commit() -> AsyncIterator[AsyncSession]:
    """Получение сессии для зависимостей FastAPI с комитом."""
    # This is Fastapi dependency
    # session: AsyncSession = Depends(get_session)
    async with db_manager.session_with_commit() as session:
        yield session
