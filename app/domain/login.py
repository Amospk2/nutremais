from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from ..utils.deps import SessionDep
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from ..models.models import User
from sqlalchemy import select
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(
    plain_password: str, 
    hashed_password: str,
    password_salt: str
):
    return pwd_context.verify(plain_password+password_salt, hashed_password)


def authenticate_user(session: SessionDep, username: str, password: str):

    user = session.execute(
        select(User).where(User.email==username)
    ).scalar_one_or_none()

    if not user:
        return False
    
    if not verify_password(password, user.password, user.password_salt):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), 
        algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


async def get_current_user(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY"), 
            algorithms=[os.getenv("ALGORITHM")]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username

    except InvalidTokenError:
        raise credentials_exception
    
    user = session.execute(
        select(User).where(User.email==token_data)
    ).scalar_one_or_none()

    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

