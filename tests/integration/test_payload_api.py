from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from app.consts import PAYLOAD_CREATED_MESSAGE, PAYLOAD_EXAMPLE, PAYLOAD_EXISTS_MESSAGE
from tests.fakes import CountingTransformer

EXPECTED_OUTPUT = (
    'FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING'
)


async def test_created_payload_can_be_read_back(
    client: AsyncClient, transformer: CountingTransformer
) -> None:
    created = await client.post('/payload', json=PAYLOAD_EXAMPLE)

    assert created.status_code == status.HTTP_201_CREATED
    assert created.json()['message'] == PAYLOAD_CREATED_MESSAGE
    read = await client.get(f'/payload/{created.json()["id"]}')
    assert read.status_code == status.HTTP_200_OK
    assert read.json() == {'output': EXPECTED_OUTPUT}
    assert len(transformer.calls) == 6


async def test_repeated_request_returns_same_id_without_calling_transformer(
    client: AsyncClient, transformer: CountingTransformer
) -> None:
    first = await client.post('/payload', json=PAYLOAD_EXAMPLE)
    calls_after_first = len(transformer.calls)

    second = await client.post('/payload', json=PAYLOAD_EXAMPLE)

    assert second.status_code == status.HTTP_200_OK
    assert second.json() == {'id': first.json()['id'], 'message': PAYLOAD_EXISTS_MESSAGE}
    assert len(transformer.calls) == calls_after_first


async def test_only_unseen_strings_are_transformed(
    client: AsyncClient, transformer: CountingTransformer
) -> None:
    await client.post('/payload', json={'list_1': ['a', ''], 'list_2': ['b', 'a']})
    transformer.calls.clear()

    response = await client.post(
        '/payload', json={'list_1': ['a', 'c', ''], 'list_2': ['', 'b', 'd']}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert sorted(transformer.calls) == ['c', 'd']
    read = await client.get(f'/payload/{response.json()["id"]}')
    assert read.json() == {'output': 'A, , C, B, , D'}


async def test_different_item_boundaries_give_different_payloads(client: AsyncClient) -> None:
    joined = await client.post('/payload', json={'list_1': ['a, b'], 'list_2': ['c']})
    split = await client.post('/payload', json={'list_1': ['a'], 'list_2': ['b, c']})

    assert joined.json()['id'] != split.json()['id']


async def test_lists_of_different_length_are_rejected(client: AsyncClient) -> None:
    response = await client.post('/payload', json={'list_1': ['a'], 'list_2': ['b', 'c']})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_unknown_payload_returns_not_found(client: AsyncClient) -> None:
    response = await client.get(f'/payload/{uuid4()}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Payload not found'}
