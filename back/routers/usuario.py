from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioCreate, UsuarioOut
from models import Usuarios
from database import get_database
from http import HTTPStatus
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioOut, status_code=HTTPStatus.CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_database)):

    if (db.query(Usuarios).filter(Usuarios.email == usuario.email).first()):
        raise HTTPException(status_code=HTTPStatus.FOUND, detail="Email já cadastrado")
    
    novo_user = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        idTipoUsuario=2
    )
    
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user