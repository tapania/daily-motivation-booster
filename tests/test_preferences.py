# tests/test_preferences.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

def test_update_preferences_success(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mock_user.created_at.isoformat.return_value = "2024-01-01T00:00:00"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock the database session
    mock_db = MagicMock()
    # Mocking ORM operations
    mock_pref = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing preference
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload with valid enum value
    payload = {
        "first_name": "Updated Test",
        "user_profile": "Updated profile",
        "timezone": "UTC",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"  # Ensure this matches VoiceEnum
    }

    response = client.patch("/preferences/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    # Assuming the UserSchema returns the updated user
    assert response.json()["first_name"] == "Updated Test"
    assert response.json()["user_profile"] == "Updated profile"
    assert response.json()["timezone"] == "UTC"
    assert response.json()["preferences"]["persona"] == "Coach Carter"
    assert response.json()["preferences"]["tone"] == "Inspirational"
    assert response.json()["preferences"]["voice"] == "Ava"