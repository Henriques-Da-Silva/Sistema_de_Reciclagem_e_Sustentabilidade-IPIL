from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import ColetaCreate, ColetaOut
from models import Coletas, Usuarios, Materiais

router = APIRouter(prefix="/coletas", tags=["coletas"])

@router.post("/", response_model=ColetaOut)
def criar_coleta(coleta: ColetaCreate, db: Session = Depends(get_database)):
    usuario = db.query(Usuarios).filter(Usuarios.id == coleta.idUsuario).first()
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
    material = db.query(Materiais).filter(Materiais.id == coleta.idMaterial).first()
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material não encontrado")
    
    pontos_ganhos = int(float(coleta.quantidadeKilo) * float(material.pontos))
    
    usuario.pontuacao += int(pontos_ganhos)
    usuario.total_reciclado = float(usuario.total_reciclado) + float(coleta.quantidadeKilo)
    
    nova_coleta = Coletas(
        idUsuario=coleta.idUsuario,
        idMaterial=coleta.idMaterial,
        quantidadeKilo=coleta.quantidadeKilo,
        pontos_ganhos=pontos_ganhos
    )
    
    db.add(nova_coleta)
    db.commit()
    db.refresh(nova_coleta)
    
    return nova_coleta

@router.get("/{user_id}", response_model=list[ColetaOut])
def listar_coletas_usuario(user_id: int, db: Session = Depends(get_database)):
    coletas = db.query(Coletas).filter(Coletas.idUsuario == user_id).order_by(Coletas.dataCadastro.desc()).all()
    
    return coletas

@router.delete("/{coleta_id}")
def deletar_coleta(coleta_id: int, db: Session = Depends(get_database)):
    coleta = db.query(Coletas).filter(Coletas.id == coleta_id).first()
    
    if not coleta:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Coleta não encontrada")
    
    usuario = db.query(Usuarios).filter(Usuarios.id == coleta.idUsuario).first()
    material = db.query(Materiais).filter(Materiais.id == coleta.idMaterial).first()
    
    usuario.pontuacao -= int(coleta.pontos_ganhos)
    usuario.total_reciclado = float(usuario.total_reciclado) - float(coleta.quantidadeKilo)
    
    db.delete(coleta)
    db.commit()
    
    return {"detail": "Coleta deletada com sucesso"}