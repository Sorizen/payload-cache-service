from collections.abc import Sequence
from itertools import chain


def interleave[T](first: Sequence[T], second: Sequence[T]) -> list[T]:
    return list(chain.from_iterable(zip(first, second, strict=True)))
