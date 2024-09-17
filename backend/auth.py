# auth.py
import msal
from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils import create_access_token
from dotenv import load_dotenv
import os
import logging

load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTHORITY = os.getenv('AUTHORITY')
SCOPE = [os.getenv('SCOPE')]

msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process_token")
async def process_token(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    code = data.get('code')
    code_verifier = data.get('code_verifier')
    if not code or not code_verifier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code and code verifier are required")
    result = msal_app.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI, code_verifier=code_verifier)
    if "error" in result:
        logging.error(f"Token acquisition error: {result.get('error_description')}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error_description"))
    microsoft_id = result['id_token_claims']['oid']
    email = result['id_token_claims'].get('preferred_username')
    user = db.query(User).filter(User.microsoft_id == microsoft_id).first()
    if not user:
        user = User(
            microsoft_id=microsoft_id,
            first_name=result['id_token_claims'].get('given_name', ''),
            email=email,
            timezone='UTC'  # Default timezone
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token(data={"sub": user.id})
    return {"message": "Authentication successful", "access_token": access_token}

@router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}