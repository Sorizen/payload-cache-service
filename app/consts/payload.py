from pydantic import JsonValue

OUTPUT_SEPARATOR = ', '

MIN_LIST_ITEMS = 1
MAX_LIST_ITEMS = 1000
MAX_ITEM_LENGTH = 1000

PAYLOAD_CREATED_MESSAGE = 'Payload created'
PAYLOAD_EXISTS_MESSAGE = 'Payload already exists'
PAYLOAD_NOT_FOUND_MESSAGE = 'Payload not found'
LISTS_LENGTH_MISMATCH_MESSAGE = 'list_1 and list_2 must have the same length'

PAYLOAD_EXAMPLE: dict[str, JsonValue] = {
    'list_1': ['first string', 'second string', 'third string'],
    'list_2': ['other string', 'another string', 'last string'],
}
