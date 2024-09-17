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

@router.get("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return RedirectResponse(auth_url)

@router.get("/token")
def get_token(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code not provided")
    result = msal_app.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
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
    response = RedirectResponse(url="/")
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, secure=True)
    return response

@router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return RedirectResponse(url="/")