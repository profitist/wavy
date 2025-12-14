import asyncio
import pytest
import os
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/wavy_test"
from main import app
from app.core.database import Base, get_session
from app.models import *

DATABASE_URL_TEST = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/test"
engine_test = create_async_engine(DATABASE_URL_TEST)
sessionmaker_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker_test() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def prepare_db():
    async with engine_test.begin() as c:
        await c.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as c:
        await c.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_generator() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=ASGITransport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def user_token_factory(ac: AsyncClient):
    async def create_user(username: str = "test_user"):
        payload = {
            "username": username,
            "hashed_password": "pupupupupupupuppu",
            "description": "lalalalala",
            "phone_number": "88005553535"
        }
        await ac.post("/user/", json=payload)

        logic_data = {"username": username, "password": "pupupupupupupuppu"}
        response = await ac.post("/user/login/", json=logic_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        return token, payload
    return create_user()
