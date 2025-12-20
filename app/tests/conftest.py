import os
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:pass@127.0.0.1:5432/test"
os.environ["S3_ID"] = "нету"
os.environ["S3_SECRET"] = "нету"
os.environ["JWT_SECRET_KEY"] = "нету"
os.environ["ALGORITHM"] = "HS256"

from main import app
from app.models.user import User
from app.auth.user_validation import get_current_user

mock_user = User(
    id="1111111111111111111111111111",
    username="test",
    role="user",
    hashed_password="test",
    description="test",
    phone_number="88005553535",
    profile_picture_url=None,
)


async def override_get_current_user():
    return mock_user


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides = {}
