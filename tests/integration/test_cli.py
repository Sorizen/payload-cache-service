import json
from pathlib import Path

from app.consts import PAYLOAD_EXAMPLE
from cli.main import main
from tests.fakes import CountingTransformer

EXPECTED_OUTPUT = (
    'FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING'
)
REPEAT = 3
EXPECTED_TRANSFORMER_CALLS = 6


def test_cli_repeats_the_request_and_reuses_the_cache(
    live_server_url: str, transformer: CountingTransformer, tmp_path: Path
) -> None:
    output_file = tmp_path / 'results.jsonl'
    args = [
        '-h', live_server_url,
        '-r', str(REPEAT),
        '-j', json.dumps(PAYLOAD_EXAMPLE),
        '-o', str(output_file),
    ]  # fmt: skip

    exit_code = main(args)

    results = [json.loads(line) for line in output_file.read_text().splitlines()]
    assert exit_code == 0
    assert [result['created'] for result in results] == [True, False, False]
    assert len({result['id'] for result in results}) == 1
    assert {result['output'] for result in results} == {EXPECTED_OUTPUT}
    assert len(transformer.calls) == EXPECTED_TRANSFORMER_CALLS
