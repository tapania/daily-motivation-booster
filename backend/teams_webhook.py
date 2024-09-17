# teams_webhook.py
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')

# backend/teams_webhook.py
def send_teams_message(username, message, speech_url=None):
    try:
        payload = {
            "title": f"Motivational Speech for {username}",
            "text": message
        }
        if speech_url:
            payload["potentialAction"] = [{
                "@type": "OpenUri",
                "name": "Listen to Speech",
                "targets": [{"os": "default", "uri": speech_url}]
            }]
        headers = {'Content-Type': 'application/json'}
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Teams message sent for user {username}")
    except requests.RequestException as e:
        logging.error(f"Error sending Teams message for user {username}: {e}")