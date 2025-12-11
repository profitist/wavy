from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_user_service
from app.services.user_service import UserService as UserService
from app.auth.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_password,
)
from app.config import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/token", tags=["tokens"])
