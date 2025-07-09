from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.models.requests import UserRequest
from ..models.models import User
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from ..utils.deps import SessionDep
from typing import Annotated
from datetime import timedelta
from ..models.models import Token
import os
from ..domain.register import create
from ..domain.login import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)


router = APIRouter(tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(session: SessionDep):
    return session.execute(select(User)).scalars().all()


@router.post("/register")
async def register(session: SessionDep, request: UserRequest):
    return create(session=session, request=request)
