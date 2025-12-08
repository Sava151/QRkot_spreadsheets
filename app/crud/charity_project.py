from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def charity_id_by_name(
            self,
            charity_name: str,
            session: AsyncSession,
    ):
        charity_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_name
            )
        )
        return charity_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        min_diff = extract(
            'epoch',
            self.model.close_date - self.model.create_date
        )
        charitys = await session.execute(
            select(
                self.model.name,
                self.model.create_date,
                self.model.close_date,
                self.model.description,
            )
            .where(
                self.model.fully_invested.is_(True),
                self.model.close_date.isnot(None)
            )
            .order_by(min_diff)
        )
        charitys = charitys.all()
        res = []
        for name, create_date, close_date, description in charitys:
            time_diff = close_date - create_date
            res.append(
                {
                    "name": name,
                    "time": str(time_diff),
                    "description": description
                }
            )
        return res


charity_project_crud = CRUDCharityProject(CharityProject)
