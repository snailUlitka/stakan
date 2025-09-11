"""Pydantic schemas for files storage."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FileRequest(BaseModel):
    """Schema for files loaded to server."""

    data: bytes
    filename: str
    size: int


class FileResponse(BaseModel):
    """Schema for file from server respond."""

    id: UUID
    filename: str
    data: bytes
    size: int
    updloaded_at: datetime


class StorageResponse(BaseModel):
    """Schema for requesting all files in storage."""

    files: list[FileResponse]
    total: int
