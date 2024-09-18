# tests/test_auth.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import os

def test_login_redirect(client: TestClient):
    response = client.get("/login", allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert "location" in response.headers
    assert response.headers["location"].startswith("https://login.microsoftonline.com")

def test_callback_success(client: TestClient, mocker):
    # Mock msal acquire_token_by_authorization_code to return a successful token
    mock_msal_app = mocker.patch('backend.auth.msal_app')
    mock_msal_app.acquire_token_by_authorization_code.return_value = {
        "id_token_claims": {
            "oid": "test_oid",
            "preferred_username": "test@example.com",
            "given_name": "Test",
            "user_profile": "Test profile"
        },
        "access_token": "mock_access_token"  # Ensure access_token is present if used
    }
    # Mock create_access_token
    mock_create_token = mocker.patch('backend.auth.create_access_token', return_value="mock_access_token")
    
    response = client.get("/callback", params={"code": "test_code"}, allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == os.getenv('FRONTEND_URL', 'http://localhost:3000')
    # Check that access_token cookie is set
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] == "mock_access_token"

def test_callback_failure(client: TestClient):
    response = client.get("/callback", params={"error": "access_denied", "error_description": "User denied access"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Authentication failed: User denied access"}

def test_logout(client: TestClient):
    response = client.get("/logout", allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == os.getenv('FRONTEND_URL', 'http://localhost:3000')
    # Check that access_token cookie is deleted
    assert "access_token" not in response.cookies

def test_get_current_user_unauthenticated(client: TestClient):
    response = client.get("/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

def test_get_current_user_authenticated(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.email = "test@example.com"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mock_user.created_at.isoformat.return_value = "2024-01-01T00:00:00"

    mocker.patch('backend.auth.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    response = client.get("/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "first_name": "Test",
        "user_profile": "Test profile",
        "timezone": "UTC",
        "email": "test@example.com",
        "preferences": None,
        "schedules": [],
        "generated_speeches": [],
        "created_at": "2024-01-01T00:00:00"
    }
