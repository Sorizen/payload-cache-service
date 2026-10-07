from pathlib import Path

from cli.consts import (
    HTTP_SCHEMES,
    INPUT_NOT_FOUND_MESSAGE,
    INVALID_HOST_MESSAGE,
    OUTPUT_DIR_NOT_FOUND_MESSAGE,
    STDIO_PATH,
)
from cli.schema import PayloadInput


def validate_host(host: str) -> str:
    if not host.startswith(HTTP_SCHEMES):
        raise ValueError(INVALID_HOST_MESSAGE)
    return host.rstrip('/')


def validate_input_path(path: str | None) -> str | None:
    if not path or path == STDIO_PATH:
        return path
    if not Path(path).is_file():
        raise ValueError(INPUT_NOT_FOUND_MESSAGE.format(path=path))
    return path


def validate_output_path(path: str) -> str:
    if path == STDIO_PATH:
        return path
    parent = Path(path).parent
    if not parent.is_dir():
        raise ValueError(OUTPUT_DIR_NOT_FOUND_MESSAGE.format(path=parent))
    return path


def validate_json_payload(raw: str | None) -> str | None:
    if raw:
        PayloadInput.model_validate_json(raw)
    return raw
