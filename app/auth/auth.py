from typing import Annotated

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.config import JWT_SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_DAYS = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    if "id" in to_encode:
        to_encode["id"] = str(to_encode["id"])
    if "uuid" in to_encode:
        to_encode["uuid"] = str(to_encode["uuid"])
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    if "id" in to_encode:
        to_encode["id"] = str(to_encode["id"])
    if "uuid" in to_encode:
        to_encode["uuid"] = str(to_encode["uuid"])
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
