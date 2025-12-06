from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.schemas.shared_track_schema import ShareRequestSchema, SharedTrackResponseSchema
from app.services.sharing_service import SharingService
from app.core.dependencies import get_sharing_service

from app.auth.user_validation import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/shared_track",
    tags=["Shared Track"],
)

@router.post("/share", response_model=SharedTrackResponseSchema, status_code=status.HTTP_201_CREATED)
async def share_music(
    request: ShareRequestSchema,
    service: Annotated[SharingService, Depends(get_sharing_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return await service.share_track(
        user_id=current_user.id,
        data=request
    )