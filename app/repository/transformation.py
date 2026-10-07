from collections.abc import Collection

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Transformation
from app.schema import TransformationCreate


class TransformationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_outputs(self, input_hashes: Collection[str]) -> dict[str, str]:
        query = select(Transformation.input_hash, Transformation.output_text).where(
            Transformation.input_hash.in_(input_hashes)
        )
        rows = await self._db.execute(query)
        return dict(rows.all())

    async def add_many(self, items: Collection[TransformationCreate]) -> None:
        if not items:
            return
        statement = (
            insert(Transformation)
            .values([item.model_dump() for item in items])
            .on_conflict_do_nothing(index_elements=[Transformation.input_hash])
        )
        await self._db.execute(statement)
