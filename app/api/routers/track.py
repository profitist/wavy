import uuid

from fastapi import Depends, APIRouter, Path, status
from typing import Annotated, List


from app.shemas.track_schema import TrackSchema, TrackCreateSchema


router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
)

# Клиентские эндпоинты


@router.get("/", response_model=List[TrackSchema], status_code=status.HTTP_200_OK)
async def get_tracks(
    offset=Annotated[int, Path(default=0)], limit=Annotated[int, Path(default=10)]
):
    pass


@router.get("/{track_id}", response_model=TrackSchema, status_code=status.HTTP_200_OK)
async def get_track(track_id: uuid.UUID):
    pass


@router.get("/{name}", response_model=List[TrackSchema], status_code=status.HTTP_200_OK)
async def get_track_by_name(name: str):
    pass


# Админские эндпоинты


@router.post("/", response_model=TrackSchema, status_code=status.HTTP_201_CREATED)
async def create_track(track: TrackCreateSchema):
    pass


@router.put("/", response_model=TrackSchema, status_code=status.HTTP_201_CREATED)
async def create_track(track: TrackCreateSchema):
    pass
