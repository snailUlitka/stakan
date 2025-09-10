from src.stakan.api.v1.models.storage import FileRequest, FileResponse, StorageResponse
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from uuid import UUID
from typing import Annotated
from stakan.core.storages.qdrant import QdrantStorage


router = APIRouter()

@router.get("/", response_model=StorageResponse)
def get_storage():
    return "no storage yet"

@router.get("/{id}", response_model=FileResponse)
def get_file(id: UUID) -> ...:
    raise NotImplementedError

@router.post("/")
def post_file(file: FileRequest, storage: Annotated[QdrantStorage, Depends()]) -> HTMLResponse:
    storage.upload_file(data=file.data)

    return HTMLResponse(status_code=201)