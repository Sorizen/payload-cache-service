from pydantic import BaseModel


class TransformationCreate(BaseModel):
    input_hash: str
    input_text: str
    output_text: str
