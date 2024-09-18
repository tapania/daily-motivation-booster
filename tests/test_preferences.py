# tests/test_preferences.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

def test_update_preferences_success(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock the database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = {
        "first_name": "Updated Test",
        "user_profile": "Updated profile",
        "timezone": "UTC",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"
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

def test_update_preferences_unauthenticated(client: TestClient):
    payload = {
        "first_name": "Updated Test",
        "user_profile": "Updated profile",
        "timezone": "UTC",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"
    }
    response = client.patch("/preferences/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

def test_update_preferences_invalid_data(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Prepare payload with invalid voice
    payload = {
        "first_name": "Updated Test",
        "user_profile": "Updated profile",
        "timezone": "UTC",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "InvalidVoice"
    }

    response = client.patch("/preferences/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error
