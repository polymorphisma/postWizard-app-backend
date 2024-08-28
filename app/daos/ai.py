from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.user import Upload


class AiDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, user_data) -> Upload:
        _upload = Upload(**user_data)
        self.session.add(_upload)
        await self.session.commit()
        await self.session.refresh(_upload)
        return _upload

    async def get_by_id(self, user_id: int) -> Upload | None:
        statement = select(Upload).where(Upload.id == user_id)
        return await self.session.scalar(statement=statement)

    async def get_by_email(self, email) -> Upload | None:
        statement = select(Upload).where(Upload.email == email)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[Upload]:
        statement = select(Upload).order_by(Upload.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Upload))
        await self.session.commit()

    async def delete_by_id(self, user_id: int) -> Upload | None:
        _user = await self.get_by_id(user_id=user_id)
        statement = delete(Upload).where(Upload.id == user_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _user
