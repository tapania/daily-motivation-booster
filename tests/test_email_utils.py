# tests/test_email_utils.py
import pytest
from unittest.mock import MagicMock, patch
from backend.email_utils import send_email

def test_send_email_success(mocker):
    # Mock the EmailClient and its methods
    mock_client = MagicMock()
    mocker.patch('backend.email_utils.EmailClient.from_connection_string', return_value=mock_client)
    
    # Mock the begin_send method to return a poller with a result
    mock_poller = MagicMock()
    mock_poller.result.return_value = MagicMock(message_id="mocked_message_id")
    mock_client.begin_send.return_value = mock_poller
    
    # Call send_email
    send_email("recipient@example.com", "Test Subject", "Test Content", attachments=[])
    
    # Assertions
    mock_client.begin_send.assert_called_once()
    mock_poller.result.assert_called_once()

def test_send_email_with_attachments_success(mocker, tmp_path):
    # Mock the EmailClient and its methods
    mock_client = MagicMock()
    mocker.patch('backend.email_utils.EmailClient.from_connection_string', return_value=mock_client)
    
    # Mock the begin_send method to return a poller with a result
    mock_poller = MagicMock()
    mock_poller.result.return_value = MagicMock(message_id="mocked_message_id")
    mock_client.begin_send.return_value = mock_poller
    
    # Create a temporary file
    attachment_path = tmp_path / "attachment.txt"
    attachment_path.write_text("Attachment content")
    
    # Call send_email with attachments
    send_email("recipient@example.com", "Test Subject", "Test Content", attachments=[str(attachment_path)])
    
    # Assertions
    mock_client.begin_send.assert_called_once()
    mock_poller.result.assert_called_once()
    # Check that the attachment was read and encoded
    args, kwargs = mock_client.begin_send.call_args
    sent_message = args[0]
    assert "attachments" in sent_message
    assert len(sent_message["attachments"]) == 1
    assert sent_message["attachments"][0]["name"] == "attachment.txt"
    assert sent_message["attachments"][0]["contentType"] == "audio/wav"
    # The contentInBase64 should be base64-encoded content
    import base64
    expected_content = base64.b64encode(b"Attachment content").decode('utf-8')
    assert sent_message["attachments"][0]["contentInBase64"] == expected_content

def test_send_email_azure_error(mocker, caplog):
    # Mock the EmailClient and its methods to raise an AzureError
    mock_client = MagicMock()
    mocker.patch('backend.email_utils.EmailClient.from_connection_string', return_value=mock_client)
    mock_client.begin_send.side_effect = Exception("AzureError")
    
    # Call send_email
    with caplog.at_level('ERROR'):
        send_email("recipient@example.com", "Test Subject", "Test Content", attachments=[])
        # Check that the error was logged
        assert "Error sending email to recipient@example.com: AzureError" in caplog.text

def test_send_email_generic_error(mocker, caplog):
    # Mock the EmailClient and its methods to raise a generic exception
    mock_client = MagicMock()
    mocker.patch('backend.email_utils.EmailClient.from_connection_string', return_value=mock_client)
    mock_client.begin_send.side_effect = Exception("Generic Error")
    
    # Call send_email
    with caplog.at_level('ERROR'):
        send_email("recipient@example.com", "Test Subject", "Test Content", attachments=[])
        # Check that the error was logged
        assert "Error sending email to recipient@example.com: Generic Error" in caplog.text