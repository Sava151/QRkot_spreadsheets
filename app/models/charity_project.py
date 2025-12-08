from sqlalchemy import String, Text, Column
from sqlalchemy.orm import Mapped

from app.models.base import QrkotBase


class CharityProject(QrkotBase):
    name: Mapped[str] = Column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = Column(
        Text,
        nullable=False
    )
