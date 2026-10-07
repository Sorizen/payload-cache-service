import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from cli.consts import NO_INPUT_MESSAGE, STDIO_PATH
from cli.exceptions import CliError


def read_input(path: str) -> str:
    if path != STDIO_PATH:
        return Path(path).read_text(encoding='utf-8')
    if sys.stdin.isatty():
        raise CliError(NO_INPUT_MESSAGE)
    return sys.stdin.read()


@contextmanager
def open_output(path: str) -> Iterator[TextIO]:
    if path == STDIO_PATH:
        yield sys.stdout
        return
    with Path(path).open('w', encoding='utf-8') as output:
        yield output
