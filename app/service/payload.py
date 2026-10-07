from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import OUTPUT_SEPARATOR
from app.exceptions import PayloadNotFoundError
from app.models import Payload
from app.repository import PayloadRepository
from app.schema import PayloadCreate, PayloadCreateResult
from app.service.transformation import TransformationService
from app.utils import hash_lists, interleave


class PayloadService:
    def __init__(self, db: AsyncSession, transformation_service: TransformationService) -> None:
        self._db = db
        self._transformation_service = transformation_service
        self._repository = PayloadRepository(db)

    async def create_payload(self, data: PayloadCreate) -> PayloadCreateResult:
        input_hash = hash_lists(data.list_1, data.list_2)
        existing_id = await self._repository.get_id_by_input_hash(input_hash)
        if existing_id:
            return PayloadCreateResult(id=existing_id, created=False)

        texts = interleave(data.list_1, data.list_2)
        outputs = await self._transformation_service.transform_many(texts)
        output = OUTPUT_SEPARATOR.join(outputs[text] for text in texts)

        payload_id = await self._repository.add_if_absent(input_hash, output)
        await self._db.commit()
        if payload_id:
            return PayloadCreateResult(id=payload_id, created=True)
        return PayloadCreateResult(id=await self._get_id(input_hash), created=False)

    async def get_payload(self, payload_id: str) -> Payload:
        payload = await self._repository.get_by_id(payload_id)
        if not payload:
            raise PayloadNotFoundError
        return payload

    async def _get_id(self, input_hash: str) -> str:
        payload_id = await self._repository.get_id_by_input_hash(input_hash)
        if not payload_id:
            raise PayloadNotFoundError
        return payload_id
