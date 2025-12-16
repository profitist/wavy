import pytest
from unittest.mock import AsyncMock
from app.core.dependencies import get_user_service
from main import app


@pytest.mark.asyncio
async def test_get_user_by_username_success(ac):
    mock_serv = AsyncMock()
    fake = {
        "id": "11111111-1111-1111-1111-111111111111",
        "username": "ussssss",
        "description": "pupupu",
        "phone_number": "123333",
        "created_at": "2026-01-01T00:00:00",
    }
    mock_serv.get_by_name.return_value = fake
    app.dependency_overrides[get_user_service] = lambda: mock_serv

    response = await ac.get("/users/ussssss")
    assert response.status_code == 200
    assert response.json()["username"] == "ussssss"


@pytest.mark.asyncio
async def test_get_user_not_found(ac):
    mock_serv = AsyncMock()
    mock_serv.get_by_name.return_value = None
    app.dependency_overrides[get_user_service] = lambda: mock_serv

    response = await ac.get("/users/unknown")
    assert response.status_code == 404
