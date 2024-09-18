# tests/test_speeches.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

def test_get_public_speeches(client: TestClient, mocker):
    # Mock database query
    mock_speeches = [
        {
            "id": 1,
            "user_id": None,
            "speech_text": "Public speech 1",
            "speech_url": "https://mocked_blob_url.com/speech1.wav",
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": 2,
            "user_id": None,
            "speech_text": "Public speech 2",
            "speech_url": "https://mocked_blob_url.com/speech2.wav",
            "created_at": "2024-01-02T00:00:00"
        }
    ]
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = mock_speeches
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    response = client.get("/public_speeches")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_speeches

def test_get_my_speeches_authenticated(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.email = "test@example.com"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock database query
    mock_speeches = [
        {
            "id": 1,
            "user_id": 1,
            "speech_text": "My speech 1",
            "speech_url": "https://mocked_blob_url.com/myspeech1.wav",
            "created_at": "2024-01-03T00:00:00"
        }
    ]
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = mock_speeches
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    response = client.get("/my_speeches/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_speeches

def test_get_my_speeches_unauthenticated(client: TestClient):
    response = client.get("/my_speeches/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}