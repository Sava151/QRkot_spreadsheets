from typing import Optional

from sqlalchemy import Text, Integer, ForeignKey, Column
from sqlalchemy.orm import Mapped

from app.models.base import QrkotBase


class Donation(QrkotBase):
    comment: Mapped[Optional[str]] = Column(Text)
    user_id: Mapped[int] = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=True
    )
