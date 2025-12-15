import uuid
from typing import Annotated, List
from fastapi import Depends, HTTPException, status, APIRouter

from app.models.friendship import Friendship
from app.models.user import User as UserModel
from app.auth.user_validation import get_current_user
from app.services.friendship_service import FriendshipService
from app.core.dependencies import get_friendship_service, get_user_service
from app.schemas.friendship import FriendshipSchema
from app.services.user_service import UserService

router = APIRouter(prefix="/friendships", tags=["Friendship"])


@router.get("/", response_model=List[FriendshipSchema])
async def get_friends(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[FriendshipService, Depends(get_friendship_service)],
):
    friends = await service.get_friends(current_user)
    return friends


@router.get("/pending", response_model=FriendshipSchema)
async def get_pending_requests(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[FriendshipService, Depends(get_friendship_service)],
):
    pending_requests = await service.get_pending_requests(current_user)
    return pending_requests


@router.post("/send/{user_id}", response_model=FriendshipSchema)
async def send_friendship_request(
    user_id: uuid.UUID,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    friendship_service: Annotated[FriendshipService, Depends(get_friendship_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> FriendshipSchema:
    to_user = await user_service.get_by_id(user_id)
    if to_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User (to request) is not found",
        )
    request = await friendship_service.sent_request(current_user, to_user)
    return request


@router.post("/reject/{user_id}", response_model=FriendshipSchema)
async def reject_friendship_request(
    user_id: uuid.UUID,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    friendship_service: Annotated[FriendshipService, Depends(get_friendship_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    to_user = await user_service.get_by_id(user_id)
    if to_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User (to reject) is not found",
        )
    request = await friendship_service.reject_request(current_user, to_user)
    return request


@router.post("/accept/{user_id}", response_model=FriendshipSchema)
async def accept_friendship_request(
    user_id: uuid.UUID,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    friendship_service: Annotated[FriendshipService, Depends(get_friendship_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    to_user = await user_service.get_by_id(user_id)
    if to_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User (to accept) is not found",
        )
    request = await friendship_service.accept_request(
        from_user=current_user, to_user=to_user
    )
    return request


@router.delete("/{user_id}")
async def delete_friend(
    user_id: uuid.UUID,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    friendship_service: Annotated[FriendshipService, Depends(get_friendship_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    to_user = await user_service.get_by_id(user_id)
    if to_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User (to accept) is not found",
        )

    await friendship_service.delete_friend(
        from_user=current_user, user_to_delete=to_user
    )
    return {
        "message": "Friendship deleted",
        "deleter": current_user.username,
        "deleted": to_user.username,
    }
