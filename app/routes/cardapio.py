from fastapi import APIRouter, status

from ..models.requests import CardapioRequest
from ..utils.deps import SessionDep
from ..domain import cardapio

router = APIRouter(
    tags=["Auth"],
    prefix="/cardapio",
)


@router.get("/")
def listagem(
    session: SessionDep,
):
    return cardapio.listagem(session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cardapio(session: SessionDep, cardapio_request: CardapioRequest):
    return cardapio.create_cardapio(session, cardapio_request)


@router.put("/{cardapio_id}", status_code=status.HTTP_200_OK)
def update_cardapio(
    cardapio_id: str, session: SessionDep, cardapio_request: CardapioRequest
):
    return cardapio.update_cardapio(cardapio_id, session, cardapio_request)


@router.delete("/{cardapio_id}")
def delete_cardapio(
    cardapio_id: str,
    session: SessionDep,
):
    return cardapio.delete_cardapio(cardapio_id, session)


@router.get("/{cardapio_id}")
def get_by_id(
    cardapio_id: str,
    session: SessionDep,
):
    return cardapio.get_by_id_cardapio(cardapio_id, session)
