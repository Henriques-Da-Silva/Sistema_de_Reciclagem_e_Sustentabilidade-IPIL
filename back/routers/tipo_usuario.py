from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import TipoUsuarioCreate, TipoUsuarioOut
from models import TipoUsuario 

router = APIRouter(prefix="/tipo-usuario", tags=["Tipos de Usuarios"])