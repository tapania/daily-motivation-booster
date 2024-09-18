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

load_dotenv('.env.test')  # Load the test environment variables

# Create a new database engine for testing
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test_app.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in SQLALCHEMY_DATABASE_URL else {}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database
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

    # Mock Azure Storage clients
    mocker.patch('backend.azure_storage.BlobServiceClient')
    mocker.patch('backend.azure_storage.ContainerClient')

    # Mock upload_file_to_blob function to return a mocked URL
    mocker.patch('backend.azure_storage.upload_file_to_blob', return_value='https://mocked_blob_url.com/speech.wav')

    # Mock send_email function
    mocker.patch('backend.email_utils.send_email')

    # Similarly, mock other external dependencies as needed
