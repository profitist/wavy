import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from starlette import status

from app.models.user import User
from app.repositories.user_repository import Repository as UserRepository
from app.core.dependencies import get_user_repository
from app.auth.auth import verify_password, create_access_token, hash_password


class Service:
    """
    Сервис работы User (надо написать КУЧУ методов) (пока базовую реализацию я накидал)
    login() не ТРОГАТЬ!!!
    """

    def __init__(self, repo: Annotated[UserRepository, Depends(get_user_repository)]):
        self.repo = repo

    async def get_by_name(self, username: str) -> User:
        user = await self.repo.get_user_by_username(username)
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        return await self.repo.get_user_by_uuid(user_id)

    async def create_user(self, user: User) -> User:
        existed_user = await self.repo.get_user_by_username(user.username)
        if existed_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user.username} already exists",
            )
        await self.repo.create_user(user)

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> dict:
        user = await self.repo.get_user_by_username(form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role, "uuid": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def update_user(self, user: User) -> User:
        existed_user = await self.repo.get_user_by_username(user.username)
        if existed_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user.username} does not exist",
            )
        await self.repo.update_user(user)
