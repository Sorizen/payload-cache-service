import httpx
from starlette import status

from cli.consts import ERROR_BODY_LIMIT, PAYLOAD_PATH
from cli.exceptions import ServiceError
from cli.schema import PayloadCreation, PayloadInput


class PayloadClient:
    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def create_payload(self, payload: PayloadInput) -> PayloadCreation:
        response = self._send('POST', PAYLOAD_PATH, json=payload.model_dump())
        return PayloadCreation(
            id=response.json()['id'],
            created=response.status_code == status.HTTP_201_CREATED,
        )

    def get_output(self, payload_id: str) -> str:
        response = self._send('GET', f'{PAYLOAD_PATH}/{payload_id}')
        return str(response.json()['output'])

    def _send(
        self, method: str, path: str, json: dict[str, list[str]] | None = None
    ) -> httpx.Response:
        try:
            response = self._http.request(method, path, json=json)
        except httpx.HTTPError as error:
            raise ServiceError(f'cannot reach the service: {error}') from error
        if response.is_error:
            raise ServiceError(f'{response.status_code}: {response.text[:ERROR_BODY_LIMIT]}')
        return response
