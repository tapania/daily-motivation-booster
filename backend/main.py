# backend/main.py
import re
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
import asyncio

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
    SpeechRequest
)
from database import SessionLocal, engine, Base
from auth import router as auth_router
from utils import verify_token
from azure_storage import upload_file_to_blob
from email_utils import send_email
from utils import create_access_token

from fastapi.middleware.cors import CORSMiddleware

# Azure OpenAI and Speech imports
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from openai import AzureOpenAI

# Initialize logging
load_dotenv()

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # e.g., ["https://your-frontend-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
AZURE_SPEECH_SUBSCRIPTION_KEY = os.getenv('AZURE_SPEECH_SUBSCRIPTION_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

def get_current_user(token: str = Depends(lambda request: request.cookies.get('access_token'))):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        system_prompt += f"\nYou are a motivational coach with the following profile:\n{speech_request.persona}:{speech_request.tone}\n."
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
        speech_config.speech_synthesis_voice_name = speech_request.voice
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        filename = f"speech_{sanitize_filename(speech_request.first_name)}_{timestamp}.wav"
        audio_config = AudioOutputConfig(filename=filename)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
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
        system_prompt += f"\nYou are a motivational coach with the following profile:\n{speech_request.persona}:{speech_request.tone}\n."
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
        speech_config.speech_synthesis_voice_name = speech_request.voice
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        filename = f"speech_public_{sanitize_filename(speech_request.first_name)}_{timestamp}.wav"
        audio_config = AudioOutputConfig(filename=filename)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
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

@app.get("/public_speeches", response_model=List[GeneratedSpeechSchema])
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
