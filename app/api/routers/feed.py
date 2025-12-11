from typing import List, Annotated
from fastapi import APIRouter, Depends

from app.schemas.shared_track_schema import SharedTrackResponseSchema
from app.repositories.shared_track_repository import SharedTrackRepository
from app.repositories.friendship_repository import FriendshipRepository
from app.core.dependencies import get_shared_track_repository, get_friendship_repository

from app.auth.user_validation import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/feed", response_model=List[SharedTrackResponseSchema])
async def get_my_feed(
        share_repo: Annotated[SharedTrackRepository, Depends(get_shared_track_repository)],
        friend_repo: Annotated[FriendshipRepository, Depends(get_friendship_repository)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    friends_relations = await friend_repo.get_friends_list(current_user.id)
    friends_ids = []
    for relationship in friends_relations:
        if relationship.sender_id == current_user.id:
            friends_ids.append(relationship.receiver_id)
        else:
            friends_ids.append(relationship.sender_id)
    friends_ids.append(current_user.id)
    return await share_repo.get_last_tracks_feed(user_ids=friends_ids, limit=50)