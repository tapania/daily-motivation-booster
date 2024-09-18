# backend/scheduler.py
import asyncio
import datetime
from database import SessionLocal
from models import User, Schedule, Preference, GeneratedSpeech
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
import openai
from azure_storage import upload_file_to_blob
from email_utils import send_email
import logging
import pytz

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SPEECH_KEY = os.getenv('AZURE_SPEECH_SUBSCRIPTION_KEY')
SPEECH_REGION = os.getenv('AZURE_SERVICE_REGION')
SAS_URL = os.getenv('AZURE_CONTAINER_SAS_URL')

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_prompt(user, preferences):
    system_prompt = f"You are speaking to {user.first_name}"
    if user.user_profile:
        system_prompt += f", whose motivational profile is:\n{user.user_profile}\n"
    system_prompt += f"\nYou are a motivational coach with the following profile:\n{preferences.persona}:{preferences.tone}\n."
    prompt = f"\nPlease write a motivational speech for {user.first_name} in the {preferences.persona} style and focus on using the correct triggers from {user.first_name}'s profile to target the speech for just him/her."

    return [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

async def generate_speech(user, preferences, db):
    try:
        # Generate speech text using Azure OpenAI
        client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            api_version = "2024-02-15-preview",
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=generate_prompt(user, preferences)
        )
        speech_text = response.choices[0].message.content

        # Convert text to speech using Azure TTS
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = preferences.voice
        filename = f"speech_{user.id}_{datetime.datetime.now().isoformat()}.wav"
        audio_config = speechsdk.AudioOutputConfig(filename=filename)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.error(f"Speech synthesis failed for user {user.id}")
            return

        # Upload file to Azure Blob Storage
        blob_name = filename
        url = upload_file_to_blob(filename, blob_name)
        if not url:
            logging.error(f"Failed to upload speech for user {user.id}")
            return

        # Save to generated_speeches table
        generated_speech = GeneratedSpeech(
            user_id=user.id,
            speech_text=speech_text,
            speech_url=url
        )
        db.add(generated_speech)

        # Send email to user
        send_email(user.email, "Your Motivational Speech", "Please find your motivational speech attached.", [filename])

        # Clean up the audio file
        os.remove(filename)

        logging.info(f"Motivational speech generated and sent to user {user.id}")
    except Exception as e:
        logging.error(f"Error generating speech for user {user.id}: {e}")

def main():
    db = SessionLocal()
    now = datetime.datetime.utcnow()
    users = db.query(User).all()
    for user in users:
        try:
            user_timezone = pytz.timezone(user.timezone)
        except pytz.UnknownTimeZoneError:
            user_timezone = pytz.UTC

        user_time = now.astimezone(user_timezone)
        schedules = db.query(Schedule).filter(Schedule.user_id == user.id).all()
        for schedule in schedules:
            if user_time.strftime('%A') == schedule.day_of_week:
                if user_time.time().hour == schedule.time_of_day.hour and user_time.time().minute == schedule.time_of_day.minute:
                    preferences = db.query(Preference).filter(Preference.user_id == user.id).first()
                    if preferences:
                        asyncio.run(generate_speech(user, preferences, db))
                    else:
                        logging.warning(f"No preferences set for user {user.id}")
    db.close()

if __name__ == '__main__':
    main()