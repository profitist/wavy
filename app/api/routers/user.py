import uuid

from fastapi import Depends, APIRouter, Path, status
from typing import Annotated, List


from app.shemas.user_schema import UserSchema


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{username}")
async def get_user(username=Annotated[str, Path(max_length=20, min_length=1)]):
    pass


@router.post("/")
async def create_user(user: UserSchema):
    pass
