# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    microsoft_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    family_situation = Column(String)
    timezone = Column(String)
    email = Column(String, unique=True)
    preferences = relationship("Preference", back_populates="user", uselist=False)
    schedules = relationship("Schedule", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow)

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    persona = Column(String)
    tone = Column(String)
    voice = Column(String)
    user = relationship("User", back_populates="preferences")

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day_of_week = Column(String)
    time_of_day = Column(Time)
    user = relationship("User", back_populates="schedules")
