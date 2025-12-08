from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    charity_exist,
    check_charity,
    check_before_delete
)
from app.crud.charity_project import charity_project_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.models import Donation
from app.services.services import invest_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity = await charity_project_crud.get_multi(session)
    return all_charity


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity(
    charity: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity.name, session)
    new_charity = await charity_project_crud.create(
        charity,
        session,
        commit=False
    )
    open_donations = await charity_project_crud.not_invested(
        Donation,
        session
    )
    changed_sources = invest_funds(
        new_charity,
        open_donations
    )
    session.add_all(changed_sources)
    await session.commit()
    await session.refresh(new_charity)
    return new_charity


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity = await charity_exist(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    check_charity(charity, obj_in)
    charity = await charity_project_crud.update(
        charity,
        obj_in,
        session,
        commit=False
    )
    open_donations = await charity_project_crud.not_invested(
        Donation,
        session
    )
    changed_sources = invest_funds(
        charity,
        open_donations
    )
    session.add_all(changed_sources)
    await session.commit()
    await session.refresh(charity)
    return charity


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity = await charity_exist(project_id, session)
    check_before_delete(charity)
    charity = await charity_project_crud.remove(charity, session)
    return charity
