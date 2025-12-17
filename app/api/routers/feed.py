from fastapi import APIRouter
import uuid
from app.schemas.shared_track_schema import SharedTrackResponseSchema
from app.models.shared_track import SharedTrack


router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/", response_model=list[SharedTrackResponseSchema])
async def get_my_feed(
        self, user_id: uuid.UUID, limit: int = 20, offset: int = 0
) -> list[SharedTrack]:
    friends = await self.friend_repo.get_friends_list(user_id)
    ids = []
    for relation in friends:
        if relation.sender_id == user_id:
            ids.append(relation.receiver_id)
        else:
            ids.append(relation.sender_id)
    if not ids:
        return []
    return await self.share_repo.get_last_tracks_feed(
        user_ids=ids, limit=limit, offset=offset
    )
