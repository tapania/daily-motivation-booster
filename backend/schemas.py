# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import time, datetime
from enum import Enum

class VoiceEnum(str, Enum):
    Ava = 'Ava'
    Andrew = 'Andrew'
    Emma = 'Emma'
    Brian = 'Brian'
    Jenny = 'Jenny'
    Guy = 'Guy'
    Aria = 'Aria'
    Davis = 'Davis'
    Jane = 'Jane'
    Jason = 'Jason'
    Sara = 'Sara'
    Tony = 'Tony'
    Nancy = 'Nancy'
    Amber = 'Amber'
    Ana = 'Ana'
    Ashley = 'Ashley'
    Brandon = 'Brandon'
    Christopher = 'Christopher'
    Cora = 'Cora'
    Elizabeth = 'Elizabeth'
    Eric = 'Eric'
    Jacob = 'Jacob'
    Michelle = 'Michelle'
    Monica = 'Monica'
    Roger = 'Roger'
    Steffan = 'Steffan'

class GeneratedSpeechBase(BaseModel):
    speech_text: str
    speech_url: str

class GeneratedSpeechCreate(GeneratedSpeechBase):
    pass

class GeneratedSpeechSchema(GeneratedSpeechBase):
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
    voice: VoiceEnum

class PreferenceBase(BaseModel):
    persona: str
    tone: str
    voice: VoiceEnum

class PreferenceCreate(PreferenceBase):
    pass

class PreferenceSchema(PreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    day_of_week: str
    time_of_day: time

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleSchema(ScheduleBase):
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

class UserSchema(UserBase):
    id: int
    email: str
    preferences: Optional[PreferenceSchema] = None
    schedules: List[ScheduleSchema] = []
    generated_speeches: List[GeneratedSpeechSchema] = []
    created_at: datetime

    class Config:
        orm_mode = True

class SpeechRequest(BaseModel):
    first_name: str
    user_profile: Optional[str] = None
    persona: str
    tone: str
    voice: VoiceEnum