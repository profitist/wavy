import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette import status
from app.schemas.user_schema import UserSchema
from app.repositories.user_repository import UserRepository
from app.auth.auth import verify_password, create_access_token, hash_password
from app.services.base_service import BaseService
from app.repositories.base_repository import BaseRepo
from app.schemas.user_schema import UserUpdateSchema, UserCreateSchema
from app.models.user import User as UserModel


class UserService(BaseService[UserRepository]):
    def __init__(self, repo: BaseRepo):
        super().__init__(repository=repo)

    async def get_by_name(self, username: str) -> UserModel:
        return await self.repository.get_by_username(username)

    async def get_by_id(self, user_id: uuid.UUID) -> UserModel:
        return await self.repository.get_by_id(user_id)

    async def create_user(self, user: UserCreateSchema):
        existed_user = await self.repository.get_by_username(user.username)
        if existed_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user.username} already exists",
            )
        new_user_data = await self.repository.create(user.model_dump())
        print(new_user_data.hashed_password)
        new_user_data.hashed_password = hash_password(user.hashed_password)
        return UserSchema.model_validate(new_user_data)

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> dict:
        user = await self.repository.get_by_username(form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role, "uuid": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def update_user(self, user: UserUpdateSchema) -> UserSchema:
        existed_user = await self.repository.get_by_username(user.username)
        if existed_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user.username} does not exist",
            )
        new_user = await self.repository.update(user.id, user.model_dump())
        return UserSchema.from_orm(new_user)
