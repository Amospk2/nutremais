import logging
from ..utils.deps import SessionDep
from ..models.requests import UserRequest
from ..models.models import User, StatusPlano
import uuid
from datetime import datetime
from sqlalchemy import select
from fastapi import Response


def create(session: SessionDep, request: UserRequest):
    try:
        current_user = session.execute(
            select(User).where(User.email == request.email)
        ).scalar_one_or_none()

        if current_user:
            return Response(status_code=422, content="Email informado já existe.")

        salt = uuid.uuid4()
        user = User(
            id=str(uuid.uuid4()),
            nome=request.nome,
            data_criacao=datetime.now(),
            status_plano=StatusPlano.ATIVO,
            password=User.get_password_hash(request.password, str(salt)),
            password_salt=str(salt),
            email=request.email,
            crm=request.crm,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    except Exception as ex:
        session.rollback()
        logging.error(str(ex))
