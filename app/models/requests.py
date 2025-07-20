from datetime import datetime
from typing import List
from pydantic import BaseModel
from .models import TipoCardapio


class UserRequest(BaseModel):
    nome: str
    password: str
    email: str
    crn: str


class ItemCardapioRequest(BaseModel):
    tipo: TipoCardapio
    titulo: str
    descricao: str


class CardapioRequest(BaseModel):
    titulo: str
    nome_paciente: str
    data: datetime
    objetivo_nutricional: str
    descricao: str

    items: List[ItemCardapioRequest]

    class Config:
        orm_mode = True
