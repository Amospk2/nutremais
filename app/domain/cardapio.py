from ..utils.deps import SessionDep
from ..models.requests import CardapioRequest
from ..models.models import Cardapio, ItemCardapio
from fastapi import Response
from sqlalchemy import update, select, delete
from sqlalchemy.orm import selectinload
import uuid
import logging


def listagem(
    session: SessionDep,
):
    try:
        return (
            session.execute(
                select(Cardapio).options(selectinload(Cardapio.items_cardapio))
            )
            .scalars()
            .all()
        )

    except Exception as ex:
        logging.error(ex)


def create_cardapio(
    session: SessionDep,
    cardapio_request: CardapioRequest,
):
    try:
        cardapio_id = str(uuid.uuid4())

        cardapio = Cardapio(
            id=cardapio_id,
            titulo=cardapio_request.titulo,
            nome_paciente=cardapio_request.nome_paciente,
            data=cardapio_request.data,
            objetivo_nutricional=cardapio_request.objetivo_nutricional,
            descricao=cardapio_request.descricao,
        )
        session.add(cardapio)

        for item in cardapio_request.items:
            session.add(
                ItemCardapio(
                    id=str(uuid.uuid4()),
                    tipo=item.tipo,
                    titulo=item.titulo,
                    descricao=item.descricao,
                    cardapio_id=cardapio_id,
                )
            )

        session.commit()
        session.refresh(cardapio)

        return {**cardapio.__dict__, "items": cardapio.items_cardapio}
    except Exception as ex:
        logging.error(ex)
        session.rollback()


def update_cardapio(
    cardapio_id: str,
    session: SessionDep,
    cardapio_request: CardapioRequest,
):
    try:
        current = session.get(Cardapio, cardapio_id)

        if not current:
            return Response(status_code=401, content="Usuário não encontrado.")

        for item in current.items_cardapio:
            session.delete(item)

        session.execute(
            update(Cardapio)
            .where(Cardapio.id == cardapio_id)
            .values(
                titulo=cardapio_request.titulo,
                nome_paciente=cardapio_request.nome_paciente,
                data=cardapio_request.data,
                objetivo_nutricional=cardapio_request.objetivo_nutricional,
                descricao=cardapio_request.descricao,
            )
        )

        for item in cardapio_request.items:
            session.add(
                ItemCardapio(
                    id=str(uuid.uuid4()),
                    tipo=item.tipo,
                    titulo=item.titulo,
                    descricao=item.descricao,
                    cardapio_id=cardapio_id,
                )
            )

        session.commit()
        session.refresh(current)

        return {**current.__dict__, "items": current.items_cardapio}
    except Exception as ex:
        logging.error(ex)
        session.rollback()


def delete_cardapio(
    cardapio_id: str,
    session: SessionDep,
):
    try:
        session.execute(delete(Cardapio).where(Cardapio.id == cardapio_id))

        session.commit()

        return {"message": "Ok"}
    except Exception as ex:
        logging.error(ex)
        session.rollback()


def get_by_id_cardapio(
    cardapio_id: str,
    session: SessionDep,
):
    try:
        return session.get(
            Cardapio, cardapio_id, options=[selectinload(Cardapio.items_cardapio)]
        )
    except Exception as ex:
        logging.error(ex)
        session.rollback()
