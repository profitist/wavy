from typing import List, Annotated
from fastapi import APIRouter, Depends

from app.schemas.shared_track_schema import SharedTrackResponseSchema
from app.core.dependencies import get_shared_track_repository
from app.services.sharing_service import SharingService

from app.auth.user_validation import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/my_feed", response_model=List[SharedTrackResponseSchema])
async def get_my_feed(
    service: Annotated[SharingService, Depends(get_shared_track_repository)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 20,
    offset: int = 0,
):
    return await service.get_my_feed(
        user_id=current_user.id, limit=limit, offset=offset
    )
