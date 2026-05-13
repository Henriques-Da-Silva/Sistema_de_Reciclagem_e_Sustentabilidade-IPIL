from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioCreate, UsuarioOut
from models import Usuarios, TipoUsuario
from database import get_database
from http import HTTPStatus
from sqlalchemy.orm import Session

from argon2 import PasswordHasher as pH

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/users", response_model=list[UsuarioOut])
def get_usuarios(db: Session = Depends(get_database)):
    usuarios = db.query(Usuarios).all()
    return usuarios

@router.post("/", response_model=UsuarioOut, status_code=HTTPStatus.CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_database)):

    if (db.query(Usuarios).filter(Usuarios.email == usuario.email).first()):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email já cadastrado")
    
    tipo_user = db.query(TipoUsuario).filter(TipoUsuario.nome == "normal").first()
    if not tipo_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Tipo de usuário 'normal' não encontrado")
    
    novo_user = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha=pH().hash(usuario.senha),
        idTipoUsuario=tipo_user.id
    )
    
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user