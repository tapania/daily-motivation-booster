# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Time, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class VoiceEnum(enum.Enum):
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

class GeneratedSpeech(Base):
    __tablename__ = 'generated_speeches'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    speech_text = Column(Text, nullable=False)
    speech_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="generated_speeches")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    microsoft_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    user_profile = Column(String)
    timezone = Column(String)
    email = Column(String, unique=True)
    preferences = relationship("Preference", back_populates="user", uselist=False)
    schedules = relationship("Schedule", back_populates="user")
    generated_speeches = relationship("GeneratedSpeech", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow)

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    persona = Column(String)
    tone = Column(String)
    voice = Column(Enum(VoiceEnum))
    user = relationship("User", back_populates="preferences")

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day_of_week = Column(String)
    time_of_day = Column(Time)
    user = relationship("User", back_populates="schedules")