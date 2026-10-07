from typing import Annotated

from fastapi import Depends

from app.dependencies.database import DbDep
from app.dependencies.transformer import TransformerDep
from app.service import PayloadService, TransformationService


def get_payload_service(db: DbDep, transformer: TransformerDep) -> PayloadService:
    return PayloadService(db, TransformationService(db, transformer))


PayloadServiceDep = Annotated[PayloadService, Depends(get_payload_service)]
