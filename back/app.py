from fastapi import FastAPI
from routers import usuario
from routers import auth
from routers import coletas
from routers import locais_coleta

app = FastAPI()

app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(coletas.router)
app.include_router(locais_coleta.router)