from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserDB(BaseModel):
    """Класс, представляющий данные пользователя из БД."""

    id: int
    name: str
    full_name: str
    created_at: datetime
    updated_at: datetime

    class Config:  # noqa: D106
        from_attributes = True


class UserCreate(BaseModel):
    """Класс, представляющий данные пользователя при создании."""

    name: str = Field(..., min_length=1, max_length=100)
    full_name: str


class UserUpdate(BaseModel):
    """Класс, представляющий данные пользователя при обновлении."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    full_name: Optional[str] = Field(None)
