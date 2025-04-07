from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)


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
    yield


def get_fastapi_app() -> FastAPI:
    """Инициализация FastAPI.

    Returns:
        app (FastAPI): Сконфигурированное приложение FastAPI.

    """
    app = FastAPI(
        lifespan=lifespan,
    )

    app.add_middleware(FixProtocolMiddleware)

    # TODO: Добавить обработчики запросов

    return app
