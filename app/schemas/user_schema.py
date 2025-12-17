import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    hashed_password: str = Field(min_length=8, max_length=40, default="")
    description: str = Field(min_length=0, max_length=250, default="")
    phone_number: str = Field(min_length=5, max_length=15)
    created_at: datetime = Field(default_factory=datetime.now)
    user_picture_number: int = Field(default=1, ge=1, le=12)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserSchema(BaseModel):
    id: uuid.UUID
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=0, max_length=250)
    phone_number: str = Field(min_length=5, max_length=15)
    created_at: datetime = Field(default_factory=datetime.now)
    user_picture_number: int = Field(default=1, ge=1, le=12)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @field_validator('user_picture_number', mode='before')
    def validate_picture_number(cls, v: int | None):
        if v is None:
            return 1
        return v


class UserUpdateSchema(BaseModel):
    id: uuid.UUID
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=0, max_length=250)
    user_picture_number: int = Field(default=1, ge=1, le=7)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
