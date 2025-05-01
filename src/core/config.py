import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

RUN_IN_DOCKER = os.getenv('IS_DOCKER', 'not').lower() == 'docker'

BASE_DIR = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    """Класс настроек приложения."""

    app_port: int = 8000
    app_title: str = 'FastAPI application'
    app_description: str = ''
    app_version: str = '0.0.0'

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_server: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=None if RUN_IN_DOCKER else BASE_DIR / '../infra/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def database_url(self) -> str:
        """Создание строки подключения к базе данных."""
        return (
            f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@'
            f'{self.postgres_server}:{self.postgres_port}/{self.postgres_db}'
        )


settings = Settings()
