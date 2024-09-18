# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import time, datetime

class GeneratedSpeechBase(BaseModel):
    speech_text: str
    speech_url: str

class GeneratedSpeechCreate(GeneratedSpeechBase):
    pass

class GeneratedSpeech(GeneratedSpeechBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

class PreferencesUpdate(BaseModel):
    first_name: str
    user_profile: Optional[str] = None
    timezone: str
    persona: str
    tone: str
    voice: str


class PreferenceBase(BaseModel):
    persona: str
    tone: str
    voice: str

class PreferenceCreate(PreferenceBase):
    pass

class Preference(PreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    day_of_week: str
    time_of_day: time

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    user_profile: Optional[str] = None
    timezone: str

class UserCreate(UserBase):
    microsoft_id: str

class User(UserBase):
    id: int
    preferences: Optional[Preference] = None
    schedules: List[Schedule] = []

    class Config:
        orm_mode = True
