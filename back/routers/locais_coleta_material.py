from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import LocalColetaMaterialCreate, LocalColetaMaterialOut, MaterialDoLocalOut, LocalDoMaterialOut
from models import LocaisColetaMaterial, LocaisColeta, Materiais

router = APIRouter(prefix='/locais_coleta_material', tags=['Locais de Coleta Material'])

@router.post('/', response_model=LocalColetaMaterialOut, status_code=HTTPStatus.CREATED)
def definir_local_coleta_material(local_coleta_material: LocalColetaMaterialCreate, db: Session = Depends(get_database)):
    novo_local_coleta_material = LocaisColetaMaterial(
        idLocalColeta=local_coleta_material.idLocalColeta,
        idMaterial=local_coleta_material.idMaterial
    )
    
    db.add(novo_local_coleta_material)
    db.commit()
    
    db.refresh(novo_local_coleta_material)
    return novo_local_coleta_material

@router.get('/local/{local_id}', response_model=list[MaterialDoLocalOut])
def local_coleta_materiais_aceites(local_id: int, db: Session = Depends(get_database)):
    local_coleta = db.query(LocaisColeta).filter(LocaisColeta.id == local_id).first()
    
    if not local_coleta:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Local de coleta não encontrado')
    
    materiais = db.query(Materiais).join(LocaisColetaMaterial).filter(LocaisColetaMaterial.idLocalColeta == local_id).all()
    
    return materiais

@router.get('/material/{material_id}', response_model=list[LocalDoMaterialOut])
def material_locais_aceites(material_id: int, db: Session = Depends(get_database)):
    material = db.query(Materiais).filter(Materiais.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Material não encontrado')
    
    locais = db.query(LocaisColeta).join(LocaisColetaMaterial).filter(LocaisColetaMaterial.idMaterial == material_id).all()
    
    return locais