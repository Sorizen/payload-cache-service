from uuid import UUID

from fastapi import APIRouter, Response
from starlette import status

from app.consts import PAYLOAD_CREATED_MESSAGE, PAYLOAD_EXISTS_MESSAGE
from app.dependencies import PayloadServiceDep
from app.schema import ErrorResponse, PayloadCreate, PayloadCreated, PayloadOutput

router = APIRouter(tags=['payload'])


@router.post(
    '/payload',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_200_OK: {'model': PayloadCreated}},
)
async def create_payload(
    data: PayloadCreate, service: PayloadServiceDep, response: Response
) -> PayloadCreated:
    result = await service.create_payload(data)
    if result.created:
        return PayloadCreated(id=result.id, message=PAYLOAD_CREATED_MESSAGE)
    response.status_code = status.HTTP_200_OK
    return PayloadCreated(id=result.id, message=PAYLOAD_EXISTS_MESSAGE)


@router.get(
    '/payload/{payload_id}',
    responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}},
)
async def get_payload(payload_id: UUID, service: PayloadServiceDep) -> PayloadOutput:
    payload = await service.get_payload(str(payload_id))
    return PayloadOutput(output=payload.output)
