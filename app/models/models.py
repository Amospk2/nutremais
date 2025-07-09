from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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


class ItemCatalogo(Base):
    __tablename__ = "item_catalogo"

    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str]
    qtd: Mapped[float]
    tipo_refeicao: Mapped[TipoRefeicao]


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
    crm: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    @staticmethod
    def get_password_hash(password: str, salt: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password + salt)
