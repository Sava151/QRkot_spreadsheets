from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.charity_id_by_name(
        room_name, session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def charity_exist(
        project_id: int,
        session: AsyncSession
) -> Optional[CharityProject]:
    charity = await charity_project_crud.get(project_id, session)
    if not charity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой проект не найден'
        )
    return charity


def check_charity(currently, updated):
    if currently.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать"
        )
    if (updated.full_amount is not None and
            updated.full_amount < currently.invested_amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя установить требуемую сумму меньше уже вложенной"
        )


def check_before_delete(charity):
    if charity.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению"
        )
