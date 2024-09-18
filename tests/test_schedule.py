# tests/test_schedule.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

def test_set_schedule_success(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = [
        {
            "day_of_week": "Monday",
            "time_of_day": "09:00"
        },
        {
            "day_of_week": "Wednesday",
            "time_of_day": "10:00"
        }
    ]

    response = client.post("/schedule/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    # Check that the response contains the schedules
    assert len(response.json()) == 2
    assert response.json()[0]["day_of_week"] == "Monday"
    assert response.json()[0]["time_of_day"] == "09:00:00"
    assert response.json()[1]["day_of_week"] == "Wednesday"
    assert response.json()[1]["time_of_day"] == "10:00:00"

def test_set_schedule_duplicate_days(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Prepare payload with duplicate days
    payload = [
        {
            "day_of_week": "Monday",
            "time_of_day": "09:00"
        },
        {
            "day_of_week": "Monday",
            "time_of_day": "10:00"
        }
    ]

    response = client.post("/schedule/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Duplicate days in schedule"}

def test_set_schedule_invalid_day(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Prepare payload with invalid day
    payload = [
        {
            "day_of_week": "Funday",
            "time_of_day": "09:00"
        }
    ]

    response = client.post("/schedule/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid day_of_week: Funday"}

def test_get_schedule_success(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock()
    mock_user.id = 1
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock database query
    mock_schedules = [
        {
            "id": 1,
            "user_id": 1,
            "day_of_week": "Monday",
            "time_of_day": "09:00:00"
        },
        {
            "id": 2,
            "user_id": 1,
            "day_of_week": "Wednesday",
            "time_of_day": "10:00:00"
        }
    ]
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = mock_schedules
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    response = client.get("/schedule/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_schedules

def test_get_schedule_unauthenticated(client: TestClient):
    response = client.get("/schedule/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}