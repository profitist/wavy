import pytest
import uuid
from unittest.mock import AsyncMock
from main import app
from app.core.dependencies import get_track_service
from app.models.user import User
from app.auth.user_validation import get_current_admin

mock_track_response = {
    "id": str(uuid.uuid4()),
    "title": "lalala",
    "author": "pupupu",
    "platform": "yandex",
    "album_cover_url": "http://img",
    "external_link": "http://link",
}


@pytest.mark.asyncio
async def test_get_tracks_list(ac):
    mock_serv = AsyncMock()
    mock_serv.search_tracks.return_value = [mock_track_response]
    app.dependency_overrides[get_track_service] = lambda: mock_serv

    response = await ac.get("/tracks/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_create_track(ac):
    mock_serv = AsyncMock()
    mock_serv.create_track.return_value = mock_track_response
    app.dependency_overrides[get_track_service] = lambda: mock_serv

    mock_admin = User(id=uuid.uuid4(), username="adm", role="admin")
    app.dependency_overrides[get_current_admin] = lambda: mock_admin

    payload = {
        "title": "lalala",
        "author": "pupupu",
        "platform": "yandex",
        "album_cover_url": "img",
        "external_link": "link",
    }

    response = await ac.post("/tracks/", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete_track(ac):
    mock_serv = AsyncMock()
    mock_serv.delete_track.return_value = {"message": "Track deleted"}
    app.dependency_overrides[get_track_service] = lambda: mock_serv

    mock_admin = User(id=uuid.uuid4(), username="adm", role="admin")
    app.dependency_overrides[get_current_admin] = lambda: mock_admin

    track_id = uuid.uuid4()
    response = await ac.delete(f"/tracks/{track_id}")
    assert response.status_code == 200
