from fastapi import FastAPI
from .routes import login, cardapio
from .domain.login import get_current_active_user
from typing import Annotated
from fastapi import Depends
from .models.models import User


app = FastAPI()


@app.get("/")
def read_root(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return {"Hello": "World", "user": current_user}


app.include_router(login.router)
app.include_router(cardapio.router)
