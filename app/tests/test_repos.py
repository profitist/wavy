import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.repositories.base_repository import BaseRepo
from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.shared_track_repository import SharedTrackRepository
from app.models.user import User
from app.models.friendship_status import FriendshipStatus


@pytest.mark.asyncio
async def test_base_repo_create_success():
    mock_db = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    repo = BaseRepo(User, mock_db)

    attributes = {"username": "qqqqqqqq", "phone_number": "88005553535"}
    result = await repo.create(attributes)

    assert result.username == "qqqqqqqq"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_base_repo_create_error():
    mock_db = AsyncMock()
    mock_db.commit.side_effect = SQLAlchemyError("DB Error")
    repo = BaseRepo(User, mock_db)

    with pytest.raises(SQLAlchemyError):
        await repo.create({"username": "failed:("})
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_base_repo_delete():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_db.execute.return_value = mock_result
    repo = BaseRepo(User, mock_db)
    res = await repo.delete(uuid.uuid4())
    assert res is True
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_friendship_repo_get_requests():
    mock_db = AsyncMock()
    mock_row = MagicMock()
    mock_row.friendship_id = uuid.uuid4()
    mock_row.sender_id = uuid.uuid4()
    mock_row.sender_username = "sveta"
    mock_row.receiver_id = uuid.uuid4()
    mock_row.receiver_username = "bogdi"

    mock_res = MagicMock()
    mock_res.all.return_value = [mock_row]
    mock_db.execute.return_value = mock_res

    repo = FriendshipRepository(mock_db)
    res = await repo.get_requests_with_status(uuid.uuid4(), FriendshipStatus.PENDING)
    assert len(res) == 1
    assert res[0]["sender"]["username"] == "sveta"


@pytest.mark.asyncio
async def test_shared_track_feed():
    mock_db = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = ["wowowow1", "wowowow2"]
    mock_db.execute.return_value = mock_res

    repo = SharedTrackRepository(mock_db)
    res = await repo.get_last_tracks_feed([uuid.uuid4()])
    assert len(res) == 2
    assert res == ["wowowow1", "wowowow2"]


@pytest.mark.asyncio
async def test_friendship_update_status_not_found():
    mock_db = AsyncMock()
    mock_db.execute.return_value.mappings.return_value.first.return_value = None
    repo = FriendshipRepository(mock_db)
    mock_db.execute.return_value.rowcount = 0
    with pytest.raises(HTTPException) as exc:
        await repo.update_status(uuid.uuid4(), uuid.uuid4(), FriendshipStatus.ACCEPTED)
    assert exc.value.status_code == 404
