from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    validator,
    PositiveInt,
    Extra
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is not None and len(value.strip()) == 0:
            raise ValueError('Название не может быть пустым')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is not None and len(value.strip()) == 0:
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    name: str
    description: str
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
