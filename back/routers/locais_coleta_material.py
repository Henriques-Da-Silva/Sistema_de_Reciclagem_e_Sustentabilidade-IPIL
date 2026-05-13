from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from database import get_database
from schemas import LocalColetaMaterialCreate, LocalColetaMaterialOut
from models import LocaisColetaMaterial

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