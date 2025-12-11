import mimetypes
import os
import uuid

from fastapi import (
    Depends,
    APIRouter,
    Path,
    status,
    Query,
    HTTPException,
    UploadFile,
    File,
)
from typing import Annotated, List

from app.models.user import User
from app.schemas.track_schema import TrackSchema, TrackCreateSchema, TrackUpdateSchema
from app.services.track_service import TrackService
from app.core.dependencies import get_track_service
from app.auth.user_validation import get_current_admin
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
)


@router.get("/{track_id}", response_model=TrackSchema, status_code=status.HTTP_200_OK)
async def get_track(
    track_id: uuid.UUID, service: TrackService = Depends(get_track_service)
):
    result = service.get_by_id(track_id)
    return result


@router.get("/", response_model=List[TrackSchema], status_code=status.HTTP_200_OK)
async def get_track_by_зфкфьуеук(
    title: Annotated[str, Query(min_length=2)] = None,
    author: Annotated[str, Query(min_length=2)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 20,
    service: TrackService = Depends(get_track_service),
):
    db_tracks = await service.get_tracks_by_parameters(
        title=title, author=author, offset=offset, limit=limit
    )
    return db_tracks


@router.post("/", response_model=TrackSchema, status_code=status.HTTP_201_CREATED)
async def create_track(
    track: TrackCreateSchema,
    service: TrackService = Depends(get_track_service),
    _: User = Depends(get_current_admin),
):
    created_track = await service.create_track(track)
    return created_track


@router.put("/", response_model=TrackSchema, status_code=status.HTTP_201_CREATED)
async def edit_track(
    track: TrackUpdateSchema,
    service: TrackService = Depends(get_track_service),
    _: User = Depends(get_current_admin),
):
    new_track_info = await service.edit_track_info(track.id, track)
    return new_track_info


@router.delete("/{track_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_track(
    track_id: uuid.UUID,
    service: TrackService = Depends(get_track_service),
    _: User = Depends(get_current_admin),
):
    deleted_info = service.delete_track(track_id)
    return deleted_info


@router.post("/upload-cover", status_code=status.HTTP_201_CREATED)
async def upload_cover(
    file: UploadFile = File(...),
    service: TrackService = Depends(get_track_service),
    _: User = Depends(get_current_admin),
) -> dict:
    file_bytes = await file.read()
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    await service.save_song_cover(file_bytes, filename)
    return {"filename": filename, "status": "saved"}


@router.get("/download-cover/{track_uuid}", status_code=status.HTTP_200_OK)
async def download_cover(
    track_uuid: str,
    service: TrackService = Depends(get_track_service),
) -> StreamingResponse:
    file = await service.s3_client.download_bytes(filename=track_uuid)
    mime, _ = mimetypes.guess_type(track_uuid)
    mime = mime or "application/octet-stream"
    return StreamingResponse(
        iter([file]),
        media_type=mime,
    )
