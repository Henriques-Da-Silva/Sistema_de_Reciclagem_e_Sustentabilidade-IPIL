from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import TipoUsuarioCreate, TipoUsuarioOut, TipoUsuarioUpdate, TipoUsuarioUpdateOut
from models import TipoUsuario 

router = APIRouter(prefix="/tipo-usuario", tags=["Tipos de Usuarios"]) 

@router.post("/", response_model=TipoUsuarioOut, status_code=HTTPStatus.CREATED)
def create_tipo_usuario(tipo_usuario: TipoUsuarioCreate, db: Session = Depends(get_database)):
    novo_tipo_usuario = TipoUsuario(
                                    nome=tipo_usuario.nome,
                                    descricao=tipo_usuario.descricao
                                    )
    
    db.add(novo_tipo_usuario)
    db.commit()
    
    db.refresh(novo_tipo_usuario)
    return novo_tipo_usuario

@router.get("/", response_model=list[TipoUsuarioOut])
def get_tipos_usuario(db: Session = Depends(get_database)):
    tipos_user = db.query(TipoUsuario).all()
    
    return tipos_user

@router.patch("/{tipo_usuario_id}", response_model=TipoUsuarioUpdateOut)
def update_tipo_usuario(tipo_usuario_id: int, tipo_usuario: TipoUsuarioUpdate, db: Session = Depends(get_database)):
    edit_tipo_usuario = db.query(TipoUsuario).filter(TipoUsuario.id == tipo_usuario_id).first()
    
    if not edit_tipo_usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Tipo de usuário não encontrado")

    edit_tipo_usuario.nome = tipo_usuario.nome or edit_tipo_usuario.nome
    edit_tipo_usuario.descricao = tipo_usuario.descricao or edit_tipo_usuario.descricao

    db.commit()
    db.refresh(edit_tipo_usuario)
    return edit_tipo_usuario

@router.delete("/{tipo_usuario_id}", response_model=TipoUsuarioOut)
def delete_tipo_usuario(tipo_usuario_id: int, db: Session = Depends(get_database)):
    tipo_usuario = db.query(TipoUsuario).filter(TipoUsuario.id == tipo_usuario_id).first()
    
    if not tipo_usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Tipo de usuário não encontrado")

    db.delete(tipo_usuario)
    db.commit()
    
    return tipo_usuario
