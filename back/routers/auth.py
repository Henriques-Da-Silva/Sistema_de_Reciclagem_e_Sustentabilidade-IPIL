from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_database
from models import Usuarios
from schemas import LoginInput, LoginOut

from argon2 import PasswordHasher as pH
from argon2.exceptions import VerifyMismatchError
from http import HTTPStatus

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=LoginOut)
def login(dados: LoginInput, db: Session = Depends(get_database)):
    
    usuario = db.query(Usuarios).filter(Usuarios.email == dados.email).first()
    
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email** ou senha incorretos")
    
    try:
        pH().verify(usuario.senha, dados.senha)
    except VerifyMismatchError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha** incorretos")
    
    return {"mensagem": "Login efetuado com sucesso", "id": usuario.id, "nome": usuario.nome}