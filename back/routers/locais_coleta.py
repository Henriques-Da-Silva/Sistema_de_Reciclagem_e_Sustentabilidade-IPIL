from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import LocalColetaCreate, LocalColetaOut, LocalColetaUpdate, LocalColetaUpdateOut
from models import LocaisColeta

router = APIRouter(prefix="/locais-coleta", tags=["Locais de Coleta"])

@router.post("/", response_model=LocalColetaOut, status_code=HTTPStatus.CREATED)
def criar_local_coleta(local: LocalColetaCreate, db: Session = Depends(get_database)):
    novo_local = LocaisColeta(
        nome=local.nome,
        descricao=local.descricao,
        endereco=local.endereco
    )
    
    db.add(novo_local)
    db.commit()
    
    db.refresh(novo_local)
    return novo_local

@router.get("/{local_id}", response_model=LocalColetaOut)
def obter_local_coleta(local_id: int, db: Session = Depends(get_database)):
    local = db.query(LocaisColeta).filter(LocaisColeta.id == local_id).first()
    
    if not local:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Local de coleta não encontrado")
    
    return local

@router.get("/", response_model=list[LocalColetaOut])
def listar_locais_coleta(db: Session = Depends(get_database)):
    locais = db.query(LocaisColeta).all()
    
    return locais

@router.patch("/{local_id}", response_model=LocalColetaUpdateOut)
def editar_local_coleta(local_id: int, local_edit: LocalColetaUpdate, db: Session = Depends(get_database)):
    local = db.query(LocaisColeta).filter(LocaisColeta.id == local_id).first()
    
    if not local:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Local de coleta não encontrado")
    
    for campo, valor in local_edit.model_dump(exclude_unset=True).items():
        setattr(local, campo, valor)
    
    db.commit()
    
    db.refresh(local)
    return local

@router.delete("/{local_id}")
def deletar_local_coleta(local_id: int, db: Session = Depends(get_database)):
    local = db.query(LocaisColeta).filter(LocaisColeta.id == local_id).first()
    
    if not local:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Local de coleta não encontrado")

    db.delete(local)
    db.commit()
    
    return {"detail": "Local de coleta deletado com sucesso"}