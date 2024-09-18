# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
import os

from backend.main import app
from backend.database import Base, get_db

# Load test environment variables
from dotenv import load_dotenv

load_dotenv('.env.test')

# Create a new database engine for testing
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test_app.db')

# Use connect_args only for SQLite
if 'sqlite' in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop all tables before creating new ones to prevent duplication
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override for the database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Mock external services
@pytest.fixture(autouse=True)
def mock_external_services(mocker):
    # Mock MSAL ConfidentialClientApplication
    mocker.patch('backend.auth.msal.ConfidentialClientApplication')
    
    # Mock AzureOpenAI
    mocker.patch('backend.main.AzureOpenAI')
    
    # Mock Azure SpeechSynthesizer
    mocker.patch('backend.main.SpeechSynthesizer')
    
    # Mock upload_file_to_blob
    mocker.patch('backend.main.upload_file_to_blob', return_value='https://mocked_blob_url.com/speech.wav')
    
    # Mock send_email
    mocker.patch('backend.main.send_email')
    
    # Similarly, mock other external dependencies as needed