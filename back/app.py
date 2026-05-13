from fastapi import FastAPI
from routers import usuario

app = FastAPI()

app.include_router(usuario.router)