# email_utils.py
import os
from dotenv import load_dotenv
import logging
from azure.communication.email import EmailClient
from azure.core.exceptions import AzureError
import base64


load_dotenv()

CONNECTION_STRING = os.getenv('AZURE_COMMUNICATION_CONNECTION_STRING')
SENDER_ADDRESS = os.getenv('SENDER_EMAIL_ADDRESS')

def send_email(to_email, subject, content, attachments=None):
    try:
        client = EmailClient.from_connection_string(CONNECTION_STRING)

        message = {
            "senderAddress": SENDER_ADDRESS,
            "recipients": {
                "to": [{"address": to_email}],
            },
            "content": {
                "subject": subject,
                "plainText": content,
                "html": f"<html><body>{content}</body></html>"
            }
        }

        # Attach files if any
        if attachments:
            message["attachments"] = []
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                    attachment = {
                        "name": file_name,
                        "contentType": "audio/wav",
                        "contentInBase64": base64.b64encode(file_data).decode('utf-8')
                    }
                message["attachments"].append(attachment)

        poller = client.begin_send(message)
        result = poller.result()
        logging.info(f"Email sent to {to_email}. Message ID: {result.message_id}")
    except AzureError as e:
        logging.error(f"Azure error sending email to {to_email}: {e}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")