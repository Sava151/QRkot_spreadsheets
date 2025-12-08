from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.services.services import invest_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
        commit=False
    )
    open_projects = await donation_crud.not_invested(
        CharityProject,
        session
    )
    changed_sources = invest_funds(
        new_donation,
        open_projects
    )
    session.add_all(changed_sources)
    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    all_donation = await donation_crud.get_by_user(
        session=session, user=user
    )
    return all_donation
