from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models import User


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ):
        donation = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donation.scalars().all()


donation_crud = CRUDDonation(Donation)
