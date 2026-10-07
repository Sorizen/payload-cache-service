import time
from collections.abc import Iterator
from typing import TextIO

import httpx

from cli.client import PayloadClient
from cli.consts import ELAPSED_MS_DIGITS, MS_IN_SECOND, REQUEST_TIMEOUT_SECONDS, STDIO_PATH
from cli.schema import IterationResult, PayloadInput
from cli.settings import CliSettings
from cli.utils import open_output, read_input


def load_payload(settings: CliSettings) -> PayloadInput:
    if settings.json_payload:
        return PayloadInput.model_validate_json(settings.json_payload)
    return PayloadInput.model_validate_json(read_input(settings.input or STDIO_PATH))


def run_iterations(
    client: PayloadClient, payload: PayloadInput, repeat: int
) -> Iterator[IterationResult]:
    for iteration in range(1, repeat + 1):
        started = time.perf_counter()
        creation = client.create_payload(payload)
        output = client.get_output(creation.id)
        elapsed_ms = (time.perf_counter() - started) * MS_IN_SECOND
        yield IterationResult(
            iteration=iteration,
            id=creation.id,
            created=creation.created,
            elapsed_ms=round(elapsed_ms, ELAPSED_MS_DIGITS),
            output=output,
        )


def write_results(results: Iterator[IterationResult], output: TextIO) -> None:
    for result in results:
        output.write(result.model_dump_json() + '\n')
        output.flush()


def run(settings: CliSettings) -> None:
    payload = load_payload(settings)
    with (
        httpx.Client(base_url=settings.host, timeout=REQUEST_TIMEOUT_SECONDS) as http,
        open_output(settings.output) as output,
    ):
        write_results(run_iterations(PayloadClient(http), payload, settings.repeat), output)
