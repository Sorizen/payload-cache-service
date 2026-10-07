from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.clients import SimulatedTransformer
from app.settings import settings
from app.types import Transformer


@lru_cache
def get_transformer() -> Transformer:
    return SimulatedTransformer(
        latency_seconds=settings.TRANSFORMER_LATENCY_SECONDS,
        max_concurrency=settings.TRANSFORMER_MAX_CONCURRENCY,
    )


TransformerDep = Annotated[Transformer, Depends(get_transformer)]
