# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request, Path
from fastapi.responses import JSONResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
import asyncio
import re

from models import User, Preference, Schedule, GeneratedSpeech
from schemas import (
    PreferenceCreate,
    ScheduleCreate,
    UserCreate,
    UserBase,
    PreferencesUpdate,
    GeneratedSpeechCreate,
    GeneratedSpeechSchema,
    UserSchema,
    SpeechRequest,
    ScheduleSchema
)
from database import SessionLocal, engine, Base, get_db
from auth import router as auth_router
from utils import verify_token, create_access_token
from azure_storage import upload_file_to_blob
from email_utils import send_email

from fastapi.middleware.cors import CORSMiddleware

# Azure OpenAI and Speech imports
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from openai import AzureOpenAI

from typing import List  # Added for typing List

load_dotenv()

# Initialize logging
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base.metadata.create_all(bind=engine)

app = FastAPI()

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# Environment variables
AZURE_SPEECH_SUBSCRIPTION_KEY = os.getenv('AZURE_SPEECH_SUBSCRIPTION_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

def get_current_user(request: Request, db: Session = Depends(get_db)):
    if request.method == "OPTIONS":
        # Skip authentication for preflight requests
        return None
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

def sanitize_filename(filename: str, max_length: int = 32) -> str:
    # Remove invalid characters
    filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    # Truncate to max_length
    return filename[:max_length]

@app.patch("/preferences/", response_model=UserSchema)
def update_preferences(preferences: PreferencesUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        # Update user info
        user.first_name = preferences.first_name
        user.user_profile = preferences.user_profile
        user.timezone = preferences.timezone

        # Update or create preferences
        db_pref = db.query(Preference).filter(Preference.user_id == user.id).first()
        if db_pref:
            db_pref.persona = preferences.persona
            db_pref.tone = preferences.tone
            db_pref.voice = preferences.voice
        else:
            db_pref = Preference(user_id=user.id, persona=preferences.persona, tone=preferences.tone, voice=preferences.voice)
            db.add(db_pref)

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        logging.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@app.get("/voices/")
def get_voices():
    voices = [
        'Ava', 'Andrew', 'Emma', 'Brian', 'Jenny', 'Guy', 'Aria', 'Davis', 
        'Jane', 'Jason', 'Sara', 'Tony', 'Nancy', 'Amber', 'Ana', 'Ashley', 
        'Brandon', 'Christopher', 'Cora', 'Elizabeth', 'Eric', 'Jacob', 
        'Michelle', 'Monica', 'Roger', 'Steffan'
    ]
    
    return JSONResponse(content={"voices": voices})

@app.post("/generate_speech", response_model=GeneratedSpeechSchema)
async def generate_speech_endpoint(speech_request: SpeechRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        # Generate speech text
        system_prompt = f"You are speaking to {speech_request.first_name}"
        if speech_request.user_profile:
            system_prompt += f", whose motivational profile is:\n{speech_request.user_profile}\n"
        system_prompt += f"\nYou are a motivational coach with the following profile:\n{speech_request.persona}:{speech_request.tone}\n\nYou reply only in plain text.\nDon't use markdown."
        prompt = f"\nPlease write a motivational speech for {speech_request.first_name} in the {speech_request.persona} style and focus on using the correct triggers from {speech_request.first_name}'s profile to target the speech for just him/her."

        # Use Azure OpenAI to generate speech text
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        speech_text = response.choices[0].message.content

        # Convert text to speech using Azure TTS
        speech_config = SpeechConfig(subscription=AZURE_SPEECH_SUBSCRIPTION_KEY, region=AZURE_SPEECH_REGION)
        speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        speech_config.speech_synthesis_voice_name = f"en-US-{speech_request.voice}Neural"
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        filename = f"speech_{sanitize_filename(speech_request.first_name)}_{timestamp}.mp3"
        audio_config = AudioOutputConfig(filename=filename)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != ResultReason.SynthesizingAudioCompleted:
            logging.error(f"Speech synthesis failed")
            raise HTTPException(status_code=500, detail="Speech synthesis failed")

        # Upload file to Azure Blob Storage
        blob_name = filename
        url = upload_file_to_blob(filename, blob_name)
        if not url:
            raise HTTPException(status_code=500, detail="Failed to upload speech to storage")

        # Save to generated_speeches table
        generated_speech = GeneratedSpeech(
            user_id=user.id,
            speech_text=speech_text,
            speech_url=url
        )
        db.add(generated_speech)
        db.commit()
        db.refresh(generated_speech)

        # Optionally, delete local file
        os.remove(filename)

        return generated_speech
    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/generate_public_speech", response_model=GeneratedSpeechSchema)
async def generate_public_speech_endpoint(speech_request: SpeechRequest, db: Session = Depends(get_db)):
    try:
        # Generate speech text
        system_prompt = f"You are speaking to {speech_request.first_name}"
        if speech_request.user_profile:
            system_prompt += f", whose motivational profile is:\n{speech_request.user_profile}\n"
        system_prompt += f"\nYou are a motivational coach with the following profile:\n{speech_request.persona}:{speech_request.tone}\n\nYou reply only in plain text.\nDon't use markdown."
        prompt = f"\nPlease write a motivational speech for {speech_request.first_name} in the {speech_request.persona} style and focus on using the correct triggers from {speech_request.first_name}'s profile to target the speech for just him/her."

        # Use Azure OpenAI to generate speech text
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        speech_text = response.choices[0].message.content

        # Convert text to speech using Azure TTS
        speech_config = SpeechConfig(subscription=AZURE_SPEECH_SUBSCRIPTION_KEY, region=AZURE_SPEECH_REGION)
        speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        speech_config.speech_synthesis_voice_name = f"en-US-{speech_request.voice}Neural"
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        filename = f"speech_public_{sanitize_filename(speech_request.first_name)}_{timestamp}.mp3"
        audio_config = AudioOutputConfig(filename=filename)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != ResultReason.SynthesizingAudioCompleted:
            logging.error(f"Speech synthesis failed for public speech")
            raise HTTPException(status_code=500, detail="Speech synthesis failed")

        # Upload file to Azure Blob Storage
        blob_name = filename
        url = upload_file_to_blob(filename, blob_name)
        if not url:
            raise HTTPException(status_code=500, detail="Failed to upload speech to storage")

        # Save to generated_speeches table with user_id = None
        generated_speech = GeneratedSpeech(
            user_id=None,
            speech_text=speech_text,
            speech_url=url
        )
        db.add(generated_speech)
        db.commit()
        db.refresh(generated_speech)

        # Optionally, delete local file
        os.remove(filename)

        return generated_speech
    except Exception as e:
        logging.error(f"Error generating public speech: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/public_speeches/", response_model=List[GeneratedSpeechSchema])
def get_public_speeches(db: Session = Depends(get_db)):
    try:
        speeches = db.query(GeneratedSpeech).filter(GeneratedSpeech.user_id == None).all()
        return speeches
    except Exception as e:
        logging.error(f"Error fetching public speeches: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/my_speeches/", response_model=List[GeneratedSpeechSchema])
def get_my_speeches(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        speeches = db.query(GeneratedSpeech).filter(GeneratedSpeech.user_id == user.id).all()
        return speeches
    except Exception as e:
        logging.error(f"Error fetching user speeches: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/public_speeches/{speech_id}/", response_model=GeneratedSpeechSchema)
def get_public_speech(
    speech_id: int = Path(..., description="The ID of the public speech to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a single public speech by its ID.
    Public speeches have user_id set to None.
    """
    speech = db.query(GeneratedSpeech).filter(GeneratedSpeech.id == speech_id, GeneratedSpeech.user_id == None).first()
    if not speech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Public speech not found")
    return speech

@app.get("/my_speeches/{speech_id}/", response_model=GeneratedSpeechSchema)
def get_my_speech(
    speech_id: int = Path(..., description="The ID of the user's speech to retrieve"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Retrieve a single speech belonging to the authenticated user by its ID.
    """
    speech = db.query(GeneratedSpeech).filter(GeneratedSpeech.id == speech_id, GeneratedSpeech.user_id == user.id).first()
    if not speech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speech not found")
    return speech

# New Endpoints for Schedule Management

@app.post("/schedule/", response_model=List[ScheduleSchema], status_code=status.HTTP_201_CREATED)
def set_schedule(schedules: List[ScheduleCreate], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Create or update schedules for the authenticated user.
    This endpoint replaces existing schedules with the provided list.
    """
    try:
        # Validate day_of_week
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for s in schedules:
            if s.day_of_week not in valid_days:
                raise HTTPException(status_code=400, detail=f"Invalid day_of_week: {s.day_of_week}")

        # Ensure no duplicate days
        days = [s.day_of_week for s in schedules]
        if len(days) != len(set(days)):
            raise HTTPException(status_code=400, detail="Duplicate days in schedule")

        # Remove existing schedules
        db.query(Schedule).filter(Schedule.user_id == user.id).delete()

        # Add new schedules
        new_schedules = [
            Schedule(
                user_id=user.id,
                day_of_week=s.day_of_week,
                time_of_day=s.time_of_day
            ) for s in schedules
        ]
        db.add_all(new_schedules)
        db.commit()

        # Refresh to get the generated IDs
        for s in new_schedules:
            db.refresh(s)

        logging.info(f"Schedules updated for user {user.id}")

        return new_schedules
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Error setting schedules for user {user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/schedule/", response_model=List[ScheduleSchema])
def get_schedule(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Retrieve the current schedules for the authenticated user.
    """
    try:
        schedules = db.query(Schedule).filter(Schedule.user_id == user.id).all()
        return schedules
    except Exception as e:
        logging.error(f"Error fetching schedules for user {user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")