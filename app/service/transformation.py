import asyncio
from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import TransformationRepository
from app.schema import TransformationCreate
from app.types import Transformer
from app.utils import hash_text


class TransformationService:
    def __init__(self, db: AsyncSession, transformer: Transformer) -> None:
        self._db = db
        self._transformer = transformer
        self._repository = TransformationRepository(db)

    async def transform_many(self, texts: Iterable[str]) -> dict[str, str]:
        hashes = {text: hash_text(text) for text in texts}
        cached = await self._repository.get_outputs(hashes.values())
        missing = [text for text, input_hash in hashes.items() if input_hash not in cached]
        fresh = await self._transform_missing(missing)
        await self._store(fresh, hashes)
        return {
            text: cached[input_hash] if input_hash in cached else fresh[text]
            for text, input_hash in hashes.items()
        }

    async def _transform_missing(self, texts: list[str]) -> dict[str, str]:
        outputs = await asyncio.gather(*(self._transformer.transform(text) for text in texts))
        return dict(zip(texts, outputs, strict=True))

    async def _store(self, fresh: dict[str, str], hashes: dict[str, str]) -> None:
        if not fresh:
            return
        await self._repository.add_many(
            [
                TransformationCreate(input_hash=hashes[text], input_text=text, output_text=output)
                for text, output in fresh.items()
            ]
        )
        await self._db.commit()
