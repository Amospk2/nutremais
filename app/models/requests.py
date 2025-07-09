from pydantic import BaseModel


class UserRequest(BaseModel):
    nome: str
    password: str
    email: str
    crm: str
