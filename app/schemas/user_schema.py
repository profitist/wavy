import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    hashed_password: str = Field(min_length=8, max_length=40, default="")
    description: str = Field(min_length=0, max_length=250, default="")
    phone_number: str = Field(min_length=5, max_length=15)
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserSchema(BaseModel):
    # id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=0, max_length=250)
    phone_number: str = Field(min_length=5, max_length=15)
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserUpdateSchema(BaseModel):
    id: uuid.UUID
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=0, max_length=250)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
