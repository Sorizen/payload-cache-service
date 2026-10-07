from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.consts import SHA256_HEX_LENGTH
from app.models.base import Base


class Transformation(Base):
    __tablename__ = 'transformations'

    input_hash: Mapped[str] = mapped_column(String(SHA256_HEX_LENGTH), unique=True)
    input_text: Mapped[str] = mapped_column(Text)
    output_text: Mapped[str] = mapped_column(Text)
