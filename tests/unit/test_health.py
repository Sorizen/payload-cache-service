from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from starlette import status

from main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get('/health')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
