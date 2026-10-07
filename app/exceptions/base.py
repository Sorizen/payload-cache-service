from http import HTTPStatus


class BaseError(Exception):
    code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = 'Internal server error'
