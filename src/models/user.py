from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.base_model import Base


class User(Base):
    """Класс пользователя."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[Optional[str]]
