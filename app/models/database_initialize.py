from models import Base, User, StatusPlano
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def initialize():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        salt = uuid.uuid4()
        session.add(
            User(
                id=uuid.uuid4(),
                nome="amos",
                data_criacao=datetime.now(),
                status_plano=StatusPlano.ATIVO,
                password=User.get_password_hash("senhateste123", str(salt)),
                password_salt=str(salt),
                crn="",
                email="teste@gmail.com",
            )
        )
        session.commit()


initialize()
