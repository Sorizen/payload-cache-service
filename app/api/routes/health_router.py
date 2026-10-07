from fastapi import APIRouter

from app.schema import HealthResponse

STATUS_OK = 'ok'

router = APIRouter(tags=['health'])


@router.get('/health')
async def get_health() -> HealthResponse:
    return HealthResponse(status=STATUS_OK)
