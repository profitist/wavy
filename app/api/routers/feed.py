from typing import List, Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.shared_track_schema import SharedTrackResponseSchema
from app.repositories.shared_track_repository import SharedTrackRepository
from app.repositories.friendship_repository import FriendshipRepository
from app.services.user_service import UserService

from app.core.dependencies import (
    get_shared_track_repository,
    get_friendship_repository,
    get_user_service,
)

router = APIRouter()


@router.get("/feed/{user_id}", response_model=List[SharedTrackResponseSchema])
async def get_my_feed(
    user_id: str,
    share_repo: Annotated[SharedTrackRepository, Depends(get_shared_track_repository)],
    friend_repo: Annotated[FriendshipRepository, Depends(get_friendship_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        user_uuid = uuid.UUID(user_id)
        target_user = await user_service.get_by_id(user_uuid)
    except ValueError:
        target_user = await user_service.get_by_name(user_id)

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Не нашли юзера"
        )

    friends_relations = await friend_repo.get_friends_list(target_user.id)
    friends_ids = []
    for relationship in friends_relations:
        if relationship.sender_id == target_user.id:
            friends_ids.append(relationship.receiver_id)
        else:
            friends_ids.append(relationship.sender_id)
    friends_ids.append(target_user.id)
    return await share_repo.get_last_tracks_feed(user_ids=friends_ids, limit=50)
