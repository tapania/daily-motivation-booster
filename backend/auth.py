# backend/auth.py
import msal
from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils import create_access_token, verify_token
from dotenv import load_dotenv
import os
import logging
from urllib.parse import urlencode
from schemas import UserSchema

load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')  # Should point to /callback endpoint
AUTHORITY = os.getenv('AUTHORITY', 'https://login.microsoftonline.com/common')
SCOPE = [os.getenv('SCOPE', 'User.Read')]
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')  # Default to localhost for development


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
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(request: Request, response: Response, db: Session = Depends(get_db)):
    query_params = dict(request.query_params)
    code = query_params.get('code')
    state = query_params.get('state')

    if not code:
        error = query_params.get('error', 'Unknown error')
        error_description = query_params.get('error_description', '')
        logging.error(f"Authentication error: {error} - {error_description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Authentication failed: {error_description}")

    result = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    if "error" in result:
        logging.error(f"Token acquisition error: {result.get('error_description')}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error_description"))

    microsoft_id = result['id_token_claims']['oid']
    email = result['id_token_claims'].get('preferred_username')
    first_name = result['id_token_claims'].get('given_name', '')
    user_profile = result['id_token_claims'].get('user_profile', '')  # Adjust based on actual claims
    timezone = 'UTC'  # Default timezone or extract from claims if available

    user = db.query(User).filter(User.microsoft_id == microsoft_id).first()
    if not user:
        user = User(
            microsoft_id=microsoft_id,
            first_name=first_name,
            email=email,
            user_profile=user_profile,
            timezone=timezone
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.id})

    # Set the access token in a secure HTTP-only cookie
    response = RedirectResponse(url=FRONTEND_URL)  # Redirect to frontend home
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Ensure HTTPS
        samesite="lax",
        max_age=3600  # 1 hour
    )
    return response

@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url=FRONTEND_URL)  # Redirect to frontend home
    response.delete_cookie(key="access_token")
    return response

@router.get("/me")
def get_current_user_endpoint(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_data = UserSchema.from_orm(user)
    return JSONResponse(content=user_data.dict())
