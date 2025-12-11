from fastapi import Depends, APIRouter, Path, status, HTTPException
from typing import Annotated, Any

from app.schemas.user_schema import UserSchema, UserUpdateSchema, UserCreateSchema
from app.core.dependencies import get_user_service
from app.services.user_service import UserService
from app.models.user import User as UserModel
from app.auth.user_validation import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_user(
    username: str = Path(max_length=20, min_length=1),
    current_user: UserModel = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_by_name(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/", status_code=201, response_model=UserSchema)
async def create_user(
    user: UserCreateSchema, service: Annotated[UserService, Depends(get_user_service)]
):
    print('tnt')
    db_user = await service.create_user(user)
    return db_user


@router.put("/{username}/", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def edit_user(
    username: str,
    user: UserUpdateSchema,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this user",
        )
    edited_user = await service.update_user(user)
    return edited_user


@router.get("/me", status_code=status.HTTP_204_NO_CONTENT, response_model=UserSchema)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
