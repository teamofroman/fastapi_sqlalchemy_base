from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from api.endpoints import main_router, router_v1
from core.config import settings
from core.db import db_manager


class FixProtocolMiddleware(BaseHTTPMiddleware):
    """Обработка запроса."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Проверка и коррекция протокола запроса."""
        protocol = request.headers.get('X-Forwarded-Protocol', None)
        if protocol in ('http', 'https'):
            request.scope['scheme'] = protocol
        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Выполнение дествий при старте и завершении FastAPI приложения.

    Args:
        app (FastAPI): Приложение FastAPI.

    """
    db_manager.init(db_url=settings.database_url)
    yield
    await db_manager.close()


def get_fastapi_app() -> FastAPI:
    """Инициализация FastAPI.

    Returns:
        app (FastAPI): Сконфигурированное приложение FastAPI.

    """
    app = FastAPI(
        lifespan=lifespan,
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )

    app.add_middleware(FixProtocolMiddleware)

    # TODO: Добавить обработчики запросов
    app.include_router(main_router)
    app.include_router(router_v1)

    return app
