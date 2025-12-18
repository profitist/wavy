import pytest
import uuid
from unittest.mock import AsyncMock
from app.core.dependencies import get_friendship_service
from main import app

from app.schemas.friendship import FriendshipSchema
from app.schemas.user_schema import UserSchema
from app.core.dependencies import get_user_service


def make_mock_friendship(status_str="pending"):
    user_mock = UserSchema(username="yana", description="", phone_number="88005553535")
    return FriendshipSchema(sender=user_mock, receiver=user_mock, status=status_str)


@pytest.mark.asyncio
async def test_get_friends(ac):
    mock_serv = AsyncMock()
    mock_serv.get_friends.return_value = [
        make_mock_friendship("accepted"),
        make_mock_friendship("accepted"),
    ]
    app.dependency_overrides[get_friendship_service] = lambda: mock_serv

    response = await ac.get("/friendships/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_serv.get_friends.assert_called_once()


@pytest.mark.asyncio
async def test_send_friend_request(ac):
    mock_serv = AsyncMock()
    mock_serv.sent_request.return_value = make_mock_friendship("pending")

    app.dependency_overrides[get_friendship_service] = lambda: mock_serv
    target_id = uuid.uuid4()
    mock_user_service = AsyncMock()
    mock_user_service.get_by_id.return_value = True
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    response = await ac.post(f"/friendships/send/{target_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_accept_friend_request(ac):
    mock_serv = AsyncMock()
    mock_serv.accept_request.return_value = make_mock_friendship("accepted")

    app.dependency_overrides[get_friendship_service] = lambda: mock_serv
    mock_user_service = AsyncMock()
    mock_user_service.get_by_id.return_value = True
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    target_id = uuid.uuid4()

    response = await ac.post(f"/friendships/accept/{target_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


@pytest.mark.asyncio
async def test_reject_friend_request(ac):
    mock_service = AsyncMock()
    mock_service.reject_request.return_value = make_mock_friendship("rejected")

    app.dependency_overrides[get_friendship_service] = lambda: mock_service
    mock_user_service = AsyncMock()
    mock_user_service.get_by_id.return_value = True
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    target_id = uuid.uuid4()

    response = await ac.post(f"/friendships/reject/{target_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
