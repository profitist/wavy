import uuid
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user_schema import UserSchema


class FriendshipSchema(BaseModel):
    sender: UserSchema
    receiver: UserSchema
    status: bool

    model_config = ConfigDict(from_attributes=True)


class DeletedFriendshipSchema(BaseModel):
    from_user: UserSchema
    deleted_user: UserSchema

    model_config = ConfigDict(from_attributes=True)
