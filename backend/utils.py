# backend/utils.py
import os
from datetime import datetime, timedelta
import jwt
from models import User
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        user = db.query(User).options(
            joinedload(User.preferences),
            joinedload(User.schedules),
            joinedload(User.generated_speeches)
        ).filter(User.id == user_id).first()
        return user
    except jwt.PyJWTError:
        return None