import pytest
from unittest.mock import AsyncMock, MagicMock
import uuid
from app.core.dependencies import get_user_service
from app.auth.auth import hash_password
from main import app
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_register_user(ac):
    mock_serv = AsyncMock()
    mock_serv.get_by_name.return_value = None
    mock_serv.create_user.return_value = {
        "id": uuid.uuid4(),
        "username": "svetlana_lox",
        "description": "pupupupu",
        "phone_number": "11111111",
    }
    app.dependency_overrides[get_user_service] = lambda: mock_serv
    payload = {
        "username": "svetlana_lox",
        "hashed_password": "lalalalala",
        "description": "pupupupu",
        "phone_number": "11111111",
    }
    response = await ac.post("/users/", json=payload)
    assert response.status_code == 201
    assert response.json()["username"] == "svetlana_lox"


@pytest.mark.asyncio
async def test_register_existing_user_fails(ac):
    mock_serv = AsyncMock()
    mock_serv.get_by_name.return_value = True
    mock_serv.create_user.side_effect = HTTPException(
        status_code=404, detail="User already exists"
    )
    app.dependency_overrides[get_user_service] = lambda: mock_serv
    payload = {
        "username": "bogdi_lox",
        "hashed_password": "22343243214324",
        "description": "hahahahaha",
        "phone_number": "11111111",
    }
    response = await ac.post("/users/", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_login_success(ac):
    mock_serv = AsyncMock()
    real = "qqqqqqqqqq"
    hashed = hash_password(real)

    fake = MagicMock()
    fake.username = "stepastepa"
    fake.hashed_password = hashed
    fake.role = "user"
    fake.id = uuid.uuid4()

    mock_serv.get_by_name.return_value = fake
    app.dependency_overrides[get_user_service] = lambda: mock_serv
    form_data = {"username": "stepastepa", "password": real}

    response = await ac.post("/users/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
