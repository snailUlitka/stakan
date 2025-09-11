"""Module with endpoints for requesting and loading files."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.stakan.api.v1.models.storage import FileRequest, FileResponse, StorageResponse
from stakan.core.storages.qdrant import QdrantStorage

router = APIRouter()


@router.get("/", response_model=StorageResponse)
def get_storage():  # noqa: ANN201 D103
    return "no storage yet"


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: UUID) -> ...:  # noqa: D103
    raise NotImplementedError


@router.post("/")
def post_file(  # noqa: D103
    file: FileRequest, storage: Annotated[QdrantStorage, Depends()]
) -> HTMLResponse:
    storage.upload_file(data=file.data)

    return HTMLResponse(status_code=201)
