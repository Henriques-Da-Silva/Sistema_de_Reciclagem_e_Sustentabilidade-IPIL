from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import MaterialCreate, MaterialOut, MaterialUpdate, MaterialUpdateOut
from models import Materiais

router = APIRouter(prefix="/materiais", tags=["Materiais"])

@router.post("/", response_model=MaterialOut, status_code=HTTPStatus.CREATED)
def create_material(material: MaterialCreate, db: Session = Depends(get_database)):
    novo_material = Materiais(
        nome=material.nome,
        descricao=material.descricao,
        pontos=material.pontos
    )
    
    db.add(novo_material)
    db.commit()
    
    db.refresh(novo_material)
    return novo_material

@router.get("/{material_id}", response_model=MaterialOut)
def read_material(material_id: int, db: Session = Depends(get_database)):
    material = db.query(Materiais).filter(Materiais.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material não encontrado")
    
    return material

@router.get("/", response_model=list[MaterialOut])
def read_materiais(db: Session = Depends(get_database)):
    materiais = db.query(Materiais).all()
    
    return materiais

@router.patch("/{material_id}", response_model=MaterialUpdateOut)
def update_material(material_id: int, material_update: MaterialUpdate, db: Session = Depends(get_database)):
    material = db.query(Materiais).filter(Materiais.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material não encontrado")
    
    for campo, valor in material_update.model_dump(exclude_unset=True).items():
        setattr(material, campo, valor)
    
    db.commit()
    db.refresh(material)
    
    return material

@router.delete("/{material_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_material(material_id: int, db: Session = Depends(get_database)):
    material = db.query(Materiais).filter(Materiais.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material não encontrado")
    
    db.delete(material)
    db.commit()