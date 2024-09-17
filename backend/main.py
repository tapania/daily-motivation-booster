# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from azure_storage import upload_file_to_blob, list_blobs

from sqlalchemy.orm import Session
from models import User, Preference, Schedule
from schemas import PreferenceCreate, ScheduleCreate, UserCreate, UserBase
from database import SessionLocal, engine, Base
from auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from utils import verify_token
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize logging
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(token: str = Depends(lambda request: request.cookies.get('access_token'))):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = verify_token(token.split(" ")[1])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/preferences/", response_model=PreferenceCreate)
def update_preferences(preferences: PreferenceCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        db_pref = db.query(Preference).filter(Preference.user_id == user.id).first()
        if db_pref:
            db_pref.persona = preferences.persona
            db_pref.tone = preferences.tone
            db_pref.voice = preferences.voice
        else:
            db_pref = Preference(user_id=user.id, **preferences.dict())
            db.add(db_pref)
        db.commit()
        db.refresh(db_pref)
        return db_pref
    except Exception as e:
        logging.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@app.get("/voices/")
def get_voices():
    try:
        import requests
        SPEECH_KEY = os.getenv('SPEECH_KEY')
        SPEECH_REGION = os.getenv('SPEECH_REGION')

        url = f"https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/voices/list"
        headers = {"Ocp-Apim-Subscription-Key": SPEECH_KEY}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching voices: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch voices")

@app.post("/schedule/")
def set_schedule(schedules: list[ScheduleCreate], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        db.query(Schedule).filter(Schedule.user_id == user.id).delete()
        for schedule in schedules:
            db_schedule = Schedule(user_id=user.id, **schedule.dict())
            db.add(db_schedule)
        db.commit()
        return {"message": "Schedule updated"}
    except Exception as e:
        logging.error(f"Error updating schedule: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


class SpeechRequest(BaseModel):
    first_name: str
    family_situation: Optional[str] = None
    persona: str
    tone: str
    voice: str

@app.post("/generate_speech")
async def generate_speech_endpoint(speech_request: SpeechRequest):
    try:
        # Generate speech text
        prompt = f"Create a {speech_request.tone} motivational speech for {speech_request.first_name}"
        if speech_request.family_situation:
            prompt += f", who is {speech_request.family_situation}"
        prompt += f", in the style of {speech_request.persona}."

        # Use Azure OpenAI to generate speech text
        client = OpenAIClient(OPENAI_API_KEY)
        response = client.completions.create(engine="davinci", prompt=prompt, max_tokens=150)
        speech_text = response.choices[0].text.strip()

        # Convert text to speech using Azure TTS
        speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = speech_request.voice
        filename = f"speech_{datetime.datetime.now().isoformat()}.wav"
        audio_config = AudioOutputConfig(filename=filename)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(speech_text).get()
        if result.reason != result.Reason.SynthesizingAudioCompleted:
            logging.error(f"Speech synthesis failed")
            raise HTTPException(status_code=500, detail="Speech synthesis failed")

        # Upload file to Azure Blob Storage
        blob_name = filename
        url = upload_file_to_blob(filename, blob_name)
        if not url:
            raise HTTPException(status_code=500, detail="Failed to upload speech to storage")

        # Optionally, delete local file
        os.remove(filename)

        return {"speech_url": url}
    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/public_speeches")
def get_public_speeches():
    try:
        blob_urls = list_blobs()
        return {"speeches": blob_urls}
    except Exception as e:
        logging.error(f"Error fetching public speeches: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")