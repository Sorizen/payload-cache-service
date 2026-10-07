from argparse import ArgumentParser
from collections.abc import Sequence
from typing import Annotated, Self

from pydantic import AfterValidator, AliasChoices, Field, model_validator
from pydantic_settings import (
    BaseSettings,
    CliSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from cli.consts import (
    DEFAULT_HOST,
    DEFAULT_REPEAT,
    INPUT_CONFLICT_MESSAGE,
    PROG,
    STDIO_PATH,
)
from cli.utils import (
    validate_host,
    validate_input_path,
    validate_json_payload,
    validate_output_path,
)


class CliSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='forbid')

    host: Annotated[str, AfterValidator(validate_host)] = Field(
        DEFAULT_HOST,
        validation_alias=AliasChoices('host', 'h'),
        description='base URL of the service',
    )
    repeat: int = Field(
        DEFAULT_REPEAT,
        ge=1,
        validation_alias=AliasChoices('repeat', 'r'),
        description='number of iterations',
    )
    input: Annotated[str | None, AfterValidator(validate_input_path)] = Field(
        None,
        validation_alias=AliasChoices('input', 'i'),
        description='input file, "-" for stdin (the default when --json is absent)',
    )
    json_payload: Annotated[str | None, AfterValidator(validate_json_payload)] = Field(
        None,
        validation_alias=AliasChoices('json', 'j'),
        description='payload as a JSON string, e.g. \'{"list_1": ["a"], "list_2": ["b"]}\'',
    )
    output: Annotated[str, AfterValidator(validate_output_path)] = Field(
        STDIO_PATH,
        validation_alias=AliasChoices('output', 'o'),
        description='output file, "-" for stdout',
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings,)

    @model_validator(mode='after')
    def check_single_input_source(self) -> Self:
        if {'input', 'json_payload'} <= self.model_fields_set:
            raise ValueError(INPUT_CONFLICT_MESSAGE)
        return self


def parse_cli_args(args: Sequence[str]) -> CliSettings:
    parser = ArgumentParser(prog=PROG, add_help=False, allow_abbrev=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    source: CliSettingsSource[CliSettings] = CliSettingsSource(
        CliSettings, root_parser=parser, cli_parse_args=True
    )
    return CliSettings(_cli_settings_source=source(args=list(args)))
