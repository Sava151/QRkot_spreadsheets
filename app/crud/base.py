from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = True
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)

        if db_obj.invested_amount is None:
            db_obj.invested_amount = 0
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        commit: bool = True
    ):

        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        if (db_obj.invested_amount >= db_obj.full_amount and not
                db_obj.fully_invested):
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now(timezone.utc)

        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def not_invested(
        self,
        model,
        session: AsyncSession,
    ):
        separated = await session.scalars(
            select(model).where(
                model.fully_invested.is_(False)
            ).order_by(model.create_date)
        )
        return separated

    async def remove(

        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
