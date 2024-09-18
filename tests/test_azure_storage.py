# tests/test_azure_storage.py
import pytest
from unittest.mock import MagicMock, patch
from backend.azure_storage import list_blobs, upload_file_to_blob

def test_list_blobs_success(mocker):
    # Mock the container_client.list_blobs method
    mock_blob = MagicMock()
    mock_blob.name = "test_blob.txt"
    mock_container_client = MagicMock()
    mock_container_client.list_blobs.return_value = [mock_blob]
    mock_container_client.get_blob_client.return_value.url = "https://mocked_blob_url.com/test_blob.txt?sv=..."
    
    # Patch the container_client
    mocker.patch('backend.azure_storage.container_client', mock_container_client)
    
    blobs = list_blobs()
    assert blobs == ["https://mocked_blob_url.com/test_blob.txt"]
    mock_container_client.list_blobs.assert_called_once()
    mock_container_client.get_blob_client.assert_called_once_with("test_blob.txt")

def test_list_blobs_failure(mocker):
    # Mock the container_client.list_blobs to raise an exception
    mock_container_client = MagicMock()
    mock_container_client.list_blobs.side_effect = Exception("Azure Blob Storage Error")
    mocker.patch('backend.azure_storage.container_client', mock_container_client)
    
    blobs = list_blobs()
    assert blobs == []
    mock_container_client.list_blobs.assert_called_once()

def test_upload_file_to_blob_success(mocker, tmp_path):
    # Create a temporary file
    file_path = tmp_path / "test_upload.txt"
    file_path.write_text("Test content")
    
    # Mock the blob_client.upload_blob method
    mock_blob_client = MagicMock()
    mock_blob_client.url = "https://mocked_blob_url.com/test_upload.txt?sv=..."
    mock_container_client = MagicMock()
    mock_container_client.get_blob_client.return_value = mock_blob_client
    mocker.patch('backend.azure_storage.container_client', mock_container_client)
    
    url = upload_file_to_blob(str(file_path), "test_upload.txt")
    assert url == "https://mocked_blob_url.com/test_upload.txt"
    mock_container_client.get_blob_client.assert_called_once_with("test_upload.txt")
    mock_blob_client.upload_blob.assert_called_once()
    
def test_upload_file_to_blob_failure(mocker, tmp_path, caplog):
    # Create a temporary file
    file_path = tmp_path / "test_upload.txt"
    file_path.write_text("Test content")

    # Mock the blob_client.upload_blob to raise an exception
    mock_blob_client = MagicMock()
    mock_blob_client.upload_blob.side_effect = Exception("Upload Failed")
    mock_container_client = MagicMock()
    mock_container_client.get_blob_client.return_value = mock_blob_client
    mocker.patch('backend.azure_storage.container_client', mock_container_client)

    # Ensure that the logger captures ERROR level logs
    with caplog.at_level('ERROR'):
        url = upload_file_to_blob(str(file_path), "test_upload.txt")
        assert url is None
        mock_container_client.get_blob_client.assert_called_once_with("test_upload.txt")
        mock_blob_client.upload_blob.assert_called_once()
        assert "Error uploading to blob: Upload Failed" in caplog.text
