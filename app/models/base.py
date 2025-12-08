from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Integer, Boolean, DateTime, Column
from sqlalchemy.orm import Mapped

from app.core.db import Base


class QrkotBase(Base):
    __abstract__ = True
    full_amount: Mapped[int] = Column(Integer, nullable=False)
    invested_amount: Mapped[int] = Column(Integer, default=0)
    fully_invested: Mapped[bool] = Column(Boolean, default=False)
    create_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    close_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range'
        ),
    )
