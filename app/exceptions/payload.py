from http import HTTPStatus

from app.consts import PAYLOAD_NOT_FOUND_MESSAGE
from app.exceptions.base import BaseError


class PayloadNotFoundError(BaseError):
    code = HTTPStatus.NOT_FOUND
    message = PAYLOAD_NOT_FOUND_MESSAGE
