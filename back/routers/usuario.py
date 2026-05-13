from fastapi import APIRouter, Depends, HTTPException

from schemas import UsuarioCreate, UsuarioOut, UsuarioUpdate, UsuarioUpdateOut
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

@router.patch("/{user_id}", response_model=UsuarioUpdateOut, status_code=HTTPStatus.OK)
def editar_usuario(user_id: int, usuario_edit: UsuarioUpdate, db: Session = Depends(get_database)):
        editando = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        
        if not editando:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
        
        user_dados = usuario_edit.model_dump(exclude_unset=True)
        if "senha" in user_dados:
            user_dados["senha"] = pH().hash(user_dados["senha"])

        for campo, valor in user_dados.items():
            setattr(editando, campo, valor)
        
        db.commit()
        db.refresh(editando)
        return editando
    
@router.get("/{user_id}", response_model=UsuarioOut, status_code=HTTPStatus.OK)
def get_usuario(user_id: int, db: Session = Depends(get_database)):
    usuario = db.query(Usuarios).filter(Usuarios.id == user_id).first()
    
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
    return usuario

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_usuario(user_id: int, db: Session = Depends(get_database)):
    usuario = db.query(Usuarios).filter(Usuarios.id == user_id).first()
    
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
    db.delete(usuario)
    db.commit()