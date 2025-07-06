from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from typing import Annotated
from fastapi import Depends
import os


def get_session():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]