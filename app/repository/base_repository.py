from typing import Any, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utilities.exceptions import NotFoundException

C = TypeVar("C", bound=SQLModel)
U = TypeVar("U", bound=SQLModel)
M = TypeVar("M", bound=SQLModel)
F = TypeVar("F", bound=SQLModel)


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _handle_commit_exceptions(self, err: IntegrityError) -> None:
        raise err

    async def _commit_refresh_or_flush(
        self, should_commit: bool, records: list[M]
    ) -> None:
        try:
            if should_commit:
                await self.session.commit()
                for record in records:
                    await self.session.refresh(record)
            else:
                await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            self._handle_commit_exceptions(e)

    async def create_record(
        self, model: type[M], record_create: C, should_commit: bool = True
    ) -> M:
        record = model.model_validate(record_create)
        self.session.add(record)
        await self._commit_refresh_or_flush(should_commit, [record])
        return record

    async def get_records(self, model: type[M], **filters: Any) -> list[M]:
        query = select(model)
        for key, value in filters.items():
            attr = getattr(model, key)
            query = query.where(attr == value)
        result = await self.session.exec(query)  # type: ignore
        records = list(result.scalars().all())
        return records

    async def get_record(self, model: type[M], **filters: Any) -> M:
        result = await self.get_records(model, **filters)
        record = result[0] if result else None
        if record is None:
            raise NotFoundException(model.name())  # type: ignore
        return record

    async def update_record(
        self,
        model: type[M],
        record_update: U,
        should_commit: bool = True,
        **filters: Any,
    ) -> M:
        record = await self.get_record(model, **filters)
        update_dict = record_update.model_dump(exclude_none=True)
        record.sqlmodel_update(update_dict)
        self.session.add(record)
        await self._commit_refresh_or_flush(should_commit, [record])
        return record
