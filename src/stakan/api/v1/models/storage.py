from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class FileRequest(BaseModel):
    data: bytes
    filename: str
    size: int


class FileResponse(BaseModel):
    id: UUID
    filename: str
    data: bytes
    size: int
    updloaded_at: datetime
    

class StorageResponse(BaseModel):
    files: list[FileResponse]
    total: int