from pydantic import BaseModel, ConfigDict


class PayloadInput(BaseModel):
    model_config = ConfigDict(extra='forbid')

    list_1: list[str]
    list_2: list[str]


class PayloadCreation(BaseModel):
    id: str
    created: bool


class IterationResult(BaseModel):
    iteration: int
    id: str
    created: bool
    elapsed_ms: float
    output: str
