import hashlib
import json
from collections.abc import Sequence

ENCODING = 'utf-8'
JSON_SEPARATORS = (',', ':')


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode(ENCODING)).hexdigest()


def hash_lists(*lists: Sequence[str]) -> str:
    canonical = json.dumps(lists, separators=JSON_SEPARATORS, ensure_ascii=False)
    return hash_text(canonical)
