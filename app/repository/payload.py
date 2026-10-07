from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Payload


class PayloadRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, payload_id: str) -> Payload | None:
        return await self._db.get(Payload, payload_id)

    async def get_id_by_input_hash(self, input_hash: str) -> str | None:
        query = select(Payload.id).where(Payload.input_hash == input_hash)
        return await self._db.scalar(query)

    async def add_if_absent(self, input_hash: str, output: str) -> str | None:
        statement = (
            insert(Payload)
            .values(input_hash=input_hash, output=output)
            .on_conflict_do_nothing(index_elements=[Payload.input_hash])
            .returning(Payload.id)
        )
        return await self._db.scalar(statement)
