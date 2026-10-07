PROG = 'cache-cli'
DEFAULT_HOST = 'http://localhost:8000'
DEFAULT_REPEAT = 1
STDIO_PATH = '-'

EXIT_FAILURE = 1
EXIT_USAGE = 2

NO_INPUT_MESSAGE = 'no input: pass --input, --json or pipe the payload to stdin'
INPUT_CONFLICT_MESSAGE = '--input and --json are mutually exclusive'
INVALID_HOST_MESSAGE = 'host must be an http(s) URL'
INPUT_NOT_FOUND_MESSAGE = 'input file does not exist: {path}'
OUTPUT_DIR_NOT_FOUND_MESSAGE = 'output directory does not exist: {path}'
