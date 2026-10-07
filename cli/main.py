import sys
from collections.abc import Sequence

from pydantic import ValidationError

from cli.consts import EXIT_FAILURE, EXIT_USAGE
from cli.exceptions import CliError
from cli.service import run
from cli.settings import parse_cli_args
from cli.utils import format_cli_error, format_validation_error


def main(args: Sequence[str] | None = None) -> int:
    try:
        settings = parse_cli_args(sys.argv[1:] if args is None else args)
    except ValidationError as error:
        return fail(format_validation_error(error), EXIT_USAGE)
    try:
        run(settings)
    except ValidationError as error:
        return fail(format_validation_error(error), EXIT_USAGE)
    except CliError as error:
        return fail(str(error), EXIT_FAILURE)
    return 0


def fail(message: str, code: int) -> int:
    print(format_cli_error(message), file=sys.stderr)
    return code


if __name__ == '__main__':
    sys.exit(main())
