import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.shared_track_schema import ShareRequestSchema, SharedTrackResponseSchema
from app.services.sharing_service import SharingService
from app.core.dependencies import get_sharing_service

from app.auth.user_validation import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/shared_track",
    tags=["Shared Track"],
)


@router.post("/", response_model=SharedTrackResponseSchema, status_code=status.HTTP_201_CREATED)
async def share_music(
    request: ShareRequestSchema,
    service: Annotated[SharingService, Depends(get_sharing_service)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return await service.share_track(
        user_id=current_user.id,
        data=request
    )


@router.get("/user/{target_user_id}", response_model=list[SharedTrackResponseSchema])
async def get_user_shares(
    target_user_id: uuid.UUID,
    service: Annotated[SharingService, Depends(get_sharing_service)],
    limit: int = 20,
    offset: int = 0
):
    return await service.get_user_shares(target_user_id, target_user_id, limit, offset)


@router.get("/my", response_model=list[SharedTrackResponseSchema])
async def get_my_shares(
    service: Annotated[SharingService, Depends(get_sharing_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await service.get_user_shares(current_user.id)


@router.get("/{share_id}", response_model=SharedTrackResponseSchema)
async def get_single_share(
    share_id: uuid.UUID,
    service: Annotated[SharingService, Depends(get_sharing_service)],
):
    share = await service.get_share_by_id(share_id)
    if not share:
        raise HTTPException(status_code=404, detail="share not found")
    return share


@router.delete("/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_share(
        share_id: uuid.UUID,
        service: Annotated[SharingService, Depends(get_sharing_service)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        success = await service.delete_share(current_user.id, share_id)
        if not success:
            raise HTTPException(status_code=404, detail="share not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="not enough permissions")
    return None

@router.get("/feed", response_model=list[SharedTrackResponseSchema])
async def get_feed(
        service: Annotated[SharingService, Depends(get_sharing_service)],
        current_user: Annotated[User, Depends(get_current_user)],
        limit: int = 20,
        offset: int = 0
):
    return await service.get_my_feed(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
