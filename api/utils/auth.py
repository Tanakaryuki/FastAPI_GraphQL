from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import uuid
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db

load_dotenv(verbose=True)
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def hash_password(password: str) -> str:
    return CryptContext(["bcrypt"]).hash(password)


def authenticate_user(
    db: Session, username: str, password: str
) -> user_model.User | None:
    user = user_crud.read_user_by_username(db=db, username=username)
    if user is None or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: str) -> user_model.User | ValueError:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if username is None or exp is None:
            raise ValueError("Decoding failed")
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
            raise ValueError("Token has expired")
    except JWTError:
        raise ValueError("Decoding failed")
    user = user_crud.read_user_by_username(db=db, username=username)
    if user is None:
        raise ValueError("User does not exist")
    return user


def get_current_user_no_exception(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> user_model.User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if username is None or exp is None:
            return None
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
            return None
    except JWTError:
        return None
    user = user_crud.read_user_by_username(db=db, username=username)
    if user is None:
        return None
    return user


def validate_refresh_token(refresh_token: str, db: Session) -> None | ValueError:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Decoding failed")
    username: str | None = payload.get("sub")
    exp: str | None = payload.get("exp")
    if username is None or exp is None:
        raise ValueError("Decoding failed")
    if not user_crud.is_refresh_token_valid(
        db=db, refresh_token=refresh_token, username=username
    ):
        raise ValueError("Refresh token does not exist")
    if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
        raise ValueError("Refresh token has expired")
