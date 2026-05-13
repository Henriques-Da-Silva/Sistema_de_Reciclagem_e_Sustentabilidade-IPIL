from fastapi import FastAPI
from routers import usuario
from routers import auth

app = FastAPI()

app.include_router(usuario.router)
app.include_router(auth.router)