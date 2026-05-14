from fastapi import FastAPI
from routers import usuario
from routers import auth
from routers import coletas
from routers import locais_coleta
from routers import locais_coleta_material
from routers import materiais
from routers import tipo_usuario

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(coletas.router)
app.include_router(locais_coleta.router)
app.include_router(locais_coleta_material.router)
app.include_router(materiais.router)
app.include_router(tipo_usuario.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)