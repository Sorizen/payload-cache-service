from pydantic import ValidationError

from cli.consts import PROG

ERROR_PREFIX = 'Value error, '


def format_validation_error(error: ValidationError) -> str:
    return '; '.join(
        f'{".".join(str(part) for part in item["loc"])}: {item["msg"].removeprefix(ERROR_PREFIX)}'
        if item['loc']
        else item['msg'].removeprefix(ERROR_PREFIX)
        for item in error.errors()
    )


def format_cli_error(message: str) -> str:
    return f'{PROG}: error: {message}'
