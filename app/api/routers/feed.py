from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.dependencies import get_sharing_service
from app.schemas.shared_track_schema import SharedTrackResponseSchema
from app.services.sharing_service import SharingService
from app.models.user import User
from app.auth.user_validation import get_current_user


router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/", response_model=list[SharedTrackResponseSchema])
async def get_my_feed(
    service: Annotated[SharingService, Depends(get_sharing_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 20,
    offset: int = 0,
):
    return await service.get_feed_for_user(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )
