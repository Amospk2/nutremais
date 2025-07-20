from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum
from datetime import datetime
from passlib.context import CryptContext
from pydantic import BaseModel


class TipoRefeicao(Enum):
    CAFE_MANHA = 1
    ALMOCO = 2
    JANTAR = 3
    CEIA = 4


class StatusPlano(Enum):
    ATIVO = 1
    INATIVO = 0


class Base(DeclarativeBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str]
    data_criacao: Mapped[datetime]
    status_plano: Mapped[StatusPlano]
    password: Mapped[str]
    password_salt: Mapped[str]
    crn: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    @staticmethod
    def get_password_hash(password: str, salt: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password + salt)


class Cardapio(Base):
    __tablename__ = "cardapio"

    id: Mapped[str] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    nome_paciente: Mapped[str]
    data: Mapped[datetime]
    objetivo_nutricional: Mapped[str]
    descricao: Mapped[str]

    items_cardapio: Mapped[List["ItemCardapio"]] = relationship(
        back_populates="cardapio"
    )


class TipoCardapio(Enum):
    CAFE_MANHA = 1
    LANCHE_MANHA = 2
    ALMOCO = 3
    LANCHE_TARDE = 4
    CAFE_NOITE = 5
    JANTAR = 6
    CEIA = 7


class ItemCardapio(Base):
    __tablename__ = "item_cardapio"

    id: Mapped[str] = mapped_column(primary_key=True)

    tipo: Mapped[TipoCardapio]
    titulo: Mapped[str]
    descricao: Mapped[str]

    cardapio_id: Mapped[int] = mapped_column(
        ForeignKey("cardapio.id", ondelete="CASCADE")
    )
    cardapio: Mapped["Cardapio"] = relationship(back_populates="items_cardapio")
