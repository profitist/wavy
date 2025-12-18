import uuid
from typing import TYPE_CHECKING, Optional

from app.repositories.friendship_repository import FriendshipRepository
from app.schemas.shared_track_schema import ShareRequestSchema
from app.models.shared_track import SharedTrack

if TYPE_CHECKING:
    from app.repositories.track_repository import TrackRepository
    from app.repositories.shared_track_repository import SharedTrackRepository


class SharingService:
    def __init__(
        self,
        track_repo: "TrackRepository",
        share_repo: "SharedTrackRepository",
        friend_repo: "FriendshipRepository",
    ):
        self.track_repo = track_repo
        self.share_repo = share_repo
        self.friend_repo = friend_repo

    async def share_track(
        self, user_id: uuid.UUID, data: ShareRequestSchema
    ) -> SharedTrack:
        track = data.track
        existing_track = await self.track_repo.get_track_by_details(
            title=track.title, author=track.author
        )

        if existing_track:
            track_id = existing_track.id
        else:
            new_track_data = {
                "title": track.title,
                "author": track.author,
                "platform": track.platform,
            }
            created_track = await self.track_repo.create(new_track_data)
            track_id = created_track.id

        share_data = {
            "sender_id": user_id,
            "track_id": track_id,
            "description": data.description,
        }
        new_share = await self.share_repo.create(share_data)
        return await self.share_repo.get_by_id(new_share.id)

    async def get_user_shares(
        self, user_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> list[SharedTrack]:
        return await self.share_repo.get_shared_tracks_by_user(user_id, limit, offset)

    async def get_share_by_id(self, share_id: uuid.UUID) -> Optional[SharedTrack]:
        return await self.share_repo.get_by_id(share_id)

    async def delete_share(self, user_id: uuid.UUID, share_id: uuid.UUID) -> bool:
        share = await self.share_repo.get_by_id(share_id)
        if not share:
            return False
        if share.sender_id != user_id:
            raise PermissionError("You can't delete other people share")
        return await self.share_repo.delete(share_id)

    async def get_feed_for_user(
        self, user_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> list[SharedTrack]:
        friends_relations = await self.friend_repo.get_friends_list(user_id)
        ids = []
        for relation in friends_relations:
            if relation.sender_id == user_id:
                ids.append(relation.receiver_id)
            else:
                ids.append(relation.sender_id)
        ids.append(user_id)
        return await self.share_repo.get_last_tracks_feed(
            user_ids=ids, limit=limit, offset=offset
        )
