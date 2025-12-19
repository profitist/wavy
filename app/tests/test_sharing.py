import pytest
import uuid
from unittest.mock import AsyncMock
from app.core.dependencies import get_sharing_service
from main import app

valid_payload = {
    "track": {
        "title": "the best song ever",
        "author": "jesus",
        "platform": "yandex",
    },
    "description": "123123",
}


@pytest.mark.asyncio
async def test_share_track_success(ac):
    mock_serv = AsyncMock()
    mock_serv.share_track.return_value = {
        "id": uuid.uuid4(),
        "sender": {"id": uuid.uuid4(), "username": "sender", "user_picture_number": 1},
        "description": "123123",
        "created_at": "2026-01-01T00:00:00",
        "track": {
            "id": uuid.uuid4(),
            "title": "the best song ever",
            "author": "jesus",
            "platform": "yandex",
        },
    }
    app.dependency_overrides[get_sharing_service] = lambda: mock_serv

    response = await ac.post("/shared_track/", json=valid_payload)
    assert response.status_code == 201
    assert response.json()["track"]["title"] == "the best song ever"


@pytest.mark.asyncio
async def test_get_my_feed_success(ac):
    mock_serv = AsyncMock()
    mock_serv.get_feed_for_user.return_value = []
    app.dependency_overrides[get_sharing_service] = lambda: mock_serv

    response = await ac.get("/feed/")
    assert response.status_code == 200
    assert response.json() == []
