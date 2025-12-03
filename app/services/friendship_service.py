from http import HTTPStatus
from typing import Annotated, List

from fastapi import Depends, HTTPException
from starlette import status

from app.models.user import User
from app.repositories.base_repository import BaseRepo
from app.services.base_service import BaseService
from app.repositories.friendship_repository import FriendshipRepository
from app.models.friendship_status import FriendshipStatus
from app.schemas.friendship import FriendshipSchema, DeletedFriendshipSchema


class FriendshipService(BaseService[FriendshipRepository]):
    def __init__(self, repo: BaseRepo):
        super().__init__(repo)

    async def sent_request(self, from_user: User, to_user: User) -> FriendshipSchema:
        result = await self.repository.create_request(from_user.id, to_user.id)
        return FriendshipSchema(
            friendship_id=result.id,
            from_user=from_user,
            to_user=to_user,
        )

    async def accept_request(self, from_user: User, to_user: User) -> FriendshipSchema:
        result = await self.repository.update_status(
            from_user.id, to_user.id, FriendshipStatus.ACCEPTED
        )
        return FriendshipSchema(
            friendship_id=result.id,
            from_user=from_user,
            to_user=to_user,
        )

    async def reject_request(self, from_user: User, to_user: User) -> FriendshipSchema:
        result = await self.repository.update_status(
            from_user.id, to_user.id, FriendshipStatus.REJECTED
        )
        return FriendshipSchema(
            friendship_id=result.id,
            from_user=from_user,
            to_user=to_user,
        )

    async def get_friends(self, from_user: User) -> List[FriendshipSchema]:
        result = await self.repository.get_friends_list(from_user.id)
        friends = []
        for request in result:
            friends.append(
                FriendshipSchema(
                    sender=request.sender,
                    receiver=request.receiver,
                    status=FriendshipStatus.PENDING,
                )
            )
        return friends

    async def get_pending_requests(self, from_user: User) -> List[FriendshipSchema]:
        result = await self.repository.get_pending_requests(from_user.id)
        pending_requests = []
        for request in result:
            pending_requests.append(
                FriendshipSchema(
                    sender=request.sender,
                    receiver=request.receiver,
                    status=FriendshipStatus.PENDING,
                )
            )
        return pending_requests

    async def delete_friend(
        self, from_user: User, user_to_delete: User
    ) -> DeletedFriendshipSchema:
        db_friendship = await self.repository.get_friendship_between(
            from_user.id, user_to_delete.id
        )
        if db_friendship is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friendship does not exist",
            )
        await self.repository.delete(db_friendship.id)
        return DeletedFriendshipSchema(from_user=from_user, to_user=user_to_delete)
