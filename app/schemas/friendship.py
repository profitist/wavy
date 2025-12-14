import uuid
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user_schema import UserSchema


class FriendshipSchema(BaseModel):
    friendship_id: uuid.UUID
    sender: UserSchema
    receiver: UserSchema
    status: str

    model_config = ConfigDict(from_attributes=True)


class DeletedFriendshipSchema(BaseModel):
    from_user: UserSchema
    deleted_user: UserSchema
    model_config = ConfigDict(from_attributes=True)
