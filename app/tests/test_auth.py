import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    payload = {
        "username": "debil",
        "hashed_password": "123",
        "description": "альбибек",
        "phone_number": "89990000000",
    }
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "debil"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_existing_user_fails(ac: AsyncClient):
    payload = {
        "username": "durak",
        "hashed_password": "pw",
        "description": "d",
        "phone_number": "123",
    }
    await ac.post("/user/", json=payload)
    response = await ac.post("/user/", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_success(ac: AsyncClient):
    await ac.post(
        "/user/",
        json={
            "username": "lox",
            "hashed_password": "pw",
            "description": "d",
            "phone_number": "123",
        },
    )

    form_data = {"username": "lox", "password": "pw"}
    response = await ac.post("/tokens/tokens", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
