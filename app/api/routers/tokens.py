from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_user_service
from app.services.user_service import Service as UserService

router = APIRouter()


@router.post("/tokens")
async def login(
    user_service: Annotated[UserService, Depends(Depends(get_user_service))],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await user_service.login_user(form_data)
    # TO DO
