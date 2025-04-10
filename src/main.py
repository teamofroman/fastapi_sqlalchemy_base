import sys

import uvicorn
from loguru import logger

from api.fastapi_app import get_fastapi_app
from core.config import BASE_DIR, settings


def loger_config() -> None:
    """Конфигурация логирования."""
    logger.remove()
    logger.add(
        BASE_DIR / 'log/fasql.log',
        rotation='100 MB',
        retention=10,
        format='{time:DD-MM-YYYY HH:mm:ss} {level} {module} {function} {message}',
        level='INFO',
        enqueue=True,
        colorize=True,
    )
    logger.add(
        sys.stdout,
        format='<g>{time:DD-MM-YYYY HH:mm:ss}</g> <b>{level}</b> {module} {function} {message}',
        level='INFO',
        enqueue=True,
        colorize=True,
    )


if __name__ == '__main__':
    loger_config()
    logger.info('Запуск приложения.')
    uvicorn.run(get_fastapi_app(), host='0.0.0.0', port=settings.app_port)
