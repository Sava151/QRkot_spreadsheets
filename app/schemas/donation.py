from datetime import datetime

from pydantic import (
    BaseModel,
    PositiveInt
)
from typing import Optional


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    full_amount: PositiveInt
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullInfoDB(DonationBase):
    id: int
    full_amount: PositiveInt
    comment: Optional[str] = None
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True
