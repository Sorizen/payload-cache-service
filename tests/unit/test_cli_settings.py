import pytest
from pydantic import ValidationError

from cli.settings import parse_cli_args

PAYLOAD_JSON = '{"list_1": ["a"], "list_2": ["b"]}'


def test_short_flags_use_h_for_host() -> None:
    settings = parse_cli_args(['-h', 'http://service:9000/', '-r', '5', '-j', PAYLOAD_JSON])

    assert settings.host == 'http://service:9000'
    assert settings.repeat == 5
    assert settings.json_payload == PAYLOAD_JSON


def test_input_file_and_json_are_mutually_exclusive() -> None:
    with pytest.raises(ValidationError):
        parse_cli_args(['-i', '-', '-j', PAYLOAD_JSON])


def test_environment_variables_do_not_override_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('HOST', 'http://from-environment')
    monkeypatch.setenv('REPEAT', '9')

    settings = parse_cli_args([])

    assert settings.host != 'http://from-environment'
    assert settings.repeat == 1
