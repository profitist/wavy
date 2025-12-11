from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_user_service
from app.services.user_service import UserService as UserService
from app.auth.auth import verify_password, create_access_token, create_refresh_token
from app.config import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("/tokens", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    db_user = await user_service.get_by_name(form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role, "id": str(db_user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": db_user.username, "role": db_user.role, "id": str(db_user.id)}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def get_new_access_token(
    refreshed_token: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refreshed_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    db_user = await user_service.get_by_name(username)
    if db_user is None:
        raise credentials_exception
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role, "id": str(db_user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}
