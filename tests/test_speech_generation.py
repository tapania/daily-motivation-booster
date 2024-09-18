# tests/test_speech_generation.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import datetime

from backend.models import User

def test_generate_speech_success(client: TestClient, mocker):
    # Mock verify_token to return a user
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mock_user.email = "test@example.com"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock AzureOpenAI client and its response
    mock_azure_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Generated speech text"))]
    mock_azure_openai.chat.completions.create.return_value = mock_response
    mocker.patch('backend.main.AzureOpenAI', return_value=mock_azure_openai)

    # Mock SpeechSynthesizer
    mock_synthesizer = MagicMock()
    mock_synthesizer.speak_text_async.return_value.get.return_value.reason = "SynthesizingAudioCompleted"
    mocker.patch('backend.main.SpeechSynthesizer', return_value=mock_synthesizer)

    # Mock upload_file_to_blob to return a mocked URL
    mocker.patch('backend.main.upload_file_to_blob', return_value='https://mocked_blob_url.com/speech.wav')

    # Mock database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = {
        "first_name": "Test",
        "user_profile": "Test profile",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"
    }

    response = client.post("/generate_speech", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["speech_text"] == "Generated speech text"
    assert data["speech_url"] == "https://mocked_blob_url.com/speech.wav"
    assert data["user_id"] == 1

    # Assert that OpenAI was called with correct parameters
    mock_azure_openai.chat.completions.create.assert_called_once()
    args, kwargs = mock_azure_openai.chat.completions.create.call_args
    assert kwargs["model"] == os.getenv("AZURE_OPENAI_DEPLOYMENT")
    assert len(kwargs["messages"]) == 2
    assert kwargs["messages"][0]["role"] == "system"
    assert kwargs["messages"][1]["role"] == "user"

    # Assert that SpeechSynthesizer was called correctly
    mock_synthesizer.speak_text_async.assert_called_once_with("Generated speech text")

    # Assert that upload_file_to_blob was called with correct parameters
    filename = mock_synthesizer.speak_text_async.return_value.get.call_args[0][0]
    mock_upload = mocker.patch('backend.main.upload_file_to_blob')
    mock_upload.assert_called_once()

    # Assert that a GeneratedSpeech entry was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_generate_speech_synthesis_failure(client: TestClient, mocker, caplog):
    # Mock verify_token to return a user
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mock_user.email = "test@example.com"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock AzureOpenAI client and its response
    mock_azure_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Generated speech text"))]
    mock_azure_openai.chat.completions.create.return_value = mock_response
    mocker.patch('backend.main.AzureOpenAI', return_value=mock_azure_openai)

    # Mock SpeechSynthesizer to simulate failure
    mock_synthesizer = MagicMock()
    mock_synthesizer.speak_text_async.return_value.get.return_value.reason = "SynthesizingAudioFailed"
    mocker.patch('backend.main.SpeechSynthesizer', return_value=mock_synthesizer)

    # Mock upload_file_to_blob should not be called
    mock_upload = mocker.patch('backend.main.upload_file_to_blob')

    # Mock database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = {
        "first_name": "Test",
        "user_profile": "Test profile",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"
    }

    response = client.post("/generate_speech", json=payload)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Speech synthesis failed"}

    # Assert that upload_file_to_blob was not called
    mock_upload.assert_not_called()

    # Check that the error was logged
    assert "Speech synthesis failed" in caplog.text

def test_generate_speech_upload_failure(client: TestClient, mocker, caplog):
    # Mock verify_token to return a user
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.first_name = "Test"
    mock_user.user_profile = "Test profile"
    mock_user.timezone = "UTC"
    mock_user.email = "test@example.com"
    mocker.patch('backend.main.verify_token', return_value=mock_user)

    # Set access_token cookie
    client.cookies.set("access_token", "mock_access_token")

    # Mock AzureOpenAI client and its response
    mock_azure_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Generated speech text"))]
    mock_azure_openai.chat.completions.create.return_value = mock_response
    mocker.patch('backend.main.AzureOpenAI', return_value=mock_azure_openai)

    # Mock SpeechSynthesizer
    mock_synthesizer = MagicMock()
    mock_synthesizer.speak_text_async.return_value.get.return_value.reason = "SynthesizingAudioCompleted"
    mocker.patch('backend.main.SpeechSynthesizer', return_value=mock_synthesizer)

    # Mock upload_file_to_blob to return None indicating failure
    mocker.patch('backend.main.upload_file_to_blob', return_value=None)

    # Mock database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = {
        "first_name": "Test",
        "user_profile": "Test profile",
        "persona": "Coach Carter",
        "tone": "Inspirational",
        "voice": "Ava"
    }

    response = client.post("/generate_speech", json=payload)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Failed to upload speech to storage"}

    # Assert that upload_file_to_blob was called
    mock_upload = mocker.patch('backend.main.upload_file_to_blob')
    mock_upload.assert_called_once()

    # Check that the error was logged
    assert "Failed to upload speech to storage" in caplog.text

def test_generate_public_speech_success(client: TestClient, mocker):
    # Mock AzureOpenAI client and its response
    mock_azure_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Public generated speech text"))]
    mock_azure_openai.chat.completions.create.return_value = mock_response
    mocker.patch('backend.main.AzureOpenAI', return_value=mock_azure_openai)

    # Mock SpeechSynthesizer
    mock_synthesizer = MagicMock()
    mock_synthesizer.speak_text_async.return_value.get.return_value.reason = "SynthesizingAudioCompleted"
    mocker.patch('backend.main.SpeechSynthesizer', return_value=mock_synthesizer)

    # Mock upload_file_to_blob to return a mocked URL
    mocker.patch('backend.main.upload_file_to_blob', return_value='https://mocked_blob_url.com/public_speech.wav')

    # Mock database session
    mock_db = MagicMock()
    mocker.patch('backend.main.get_db', return_value=iter([mock_db]))

    # Prepare payload
    payload = {
        "first_name": "Public",
        "user_profile": "Public profile",
        "persona": "Cheerful Friend",
        "tone": "Friendly and Upbeat",
        "voice": "Jenny"
    }

    response = client.post("/generate_public_speech", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["speech_text"] == "Public generated speech text"
    assert data["speech_url"] == "https://mocked_blob_url.com/public_speech.wav"
    assert data["user_id"] is None

    # Assert that OpenAI was called with correct parameters
    mock_azure_openai.chat.completions.create.assert_called_once()

    # Assert that SpeechSynthesizer was called correctly
    mock_synthesizer.speak_text_async.assert_called_once_with("Public generated speech text")

    # Assert that upload_file_to_blob was called with correct parameters
    mock_upload = mocker.patch('backend.main.upload_file_to_blob')
    mock_upload.assert_called_once()

    # Assert that a GeneratedSpeech entry was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
