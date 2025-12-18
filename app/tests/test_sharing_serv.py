import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.services.sharing_service import SharingService
from app.schemas.shared_track_schema import ShareRequestSchema
from app.schemas.track_schema import TrackCreateSchema

track_data = TrackCreateSchema(
    title="lalala",
    author="author",
    platform="yandex",
)
share_request = ShareRequestSchema(track=track_data, description="Test")
user_id = uuid.uuid4()


@pytest.mark.asyncio
async def test_share_track_creates_new_track():
    mock_track_repo = AsyncMock()
    mock_share_repo = AsyncMock()
    mock_friend_repo = AsyncMock()

    mock_track_repo.get_tracks_by_details.return_value = []
    new_track = MagicMock()
    new_track.id = uuid.uuid4()
    mock_track_repo.create.return_value = new_track

    new_share = MagicMock()
    new_share.id = uuid.uuid4()
    mock_share_repo.create.return_value = new_share
    mock_db_result = MagicMock()
    mock_db_result.scalar_one.return_value = new_share
    mock_share_repo.db.execute.return_value = mock_db_result

    service = SharingService(mock_track_repo, mock_share_repo, mock_friend_repo)

    await service.share_track(user_id, share_request)
    mock_track_repo.create.assert_called_once()

    args = mock_track_repo.create.call_args[0][0]
    assert args["title"] == "lalala"
    mock_share_repo.create.assert_called_once()
