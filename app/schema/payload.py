from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from app.consts import (
    LISTS_LENGTH_MISMATCH_MESSAGE,
    MAX_ITEM_LENGTH,
    MAX_LIST_ITEMS,
    MIN_LIST_ITEMS,
    PAYLOAD_EXAMPLE,
)

StringList = Annotated[
    list[Annotated[str, StringConstraints(max_length=MAX_ITEM_LENGTH)]],
    Field(min_length=MIN_LIST_ITEMS, max_length=MAX_LIST_ITEMS),
]


class PayloadCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={'example': PAYLOAD_EXAMPLE})

    list_1: StringList
    list_2: StringList

    @model_validator(mode='after')
    def check_lists_have_same_length(self) -> Self:
        if len(self.list_1) != len(self.list_2):
            raise ValueError(LISTS_LENGTH_MISMATCH_MESSAGE)
        return self


class PayloadCreateResult(BaseModel):
    id: str
    created: bool


class PayloadCreated(BaseModel):
    id: str
    message: str


class PayloadOutput(BaseModel):
    output: str
