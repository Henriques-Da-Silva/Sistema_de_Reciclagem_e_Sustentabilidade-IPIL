from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Schemas para tabela usuarios
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    
class UsuarioCreate(UsuarioBase):
    senha: str
    idTipoUsuario: int
    
class UsuarioOut(UsuarioBase):
    id: int
    pontuacao: int
    total_reciclado: float
    created_at: datetime
    
    class Config:
        from_attributes = True
        
# Schemas para tabela coletas
class ColetaBase(BaseModel):
    idUsuario: int
    idMaterial: int
    quantidadeKilo: float

class ColetaCreate(ColetaBase):
    pass

class ColetaOut(ColetaBase):
    id: int
    pontos_ganhos: int
    dataCadastro: datetime

    class Config:
        from_attributes = True
        
# Schemas para tabela locais_coleta
class LocalColetaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    endereco: Optional[str] = None

class LocalColetaCreate(LocalColetaBase):
    pass

class LocalColetaOut(LocalColetaBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True

# Schemas para tabela locais_coleta_material
class LocalColetaMaterialBase(BaseModel):
    idLocalColeta: int
    idMaterial: int

class LocalColetaMaterialCreate(LocalColetaMaterialBase):
    pass

class LocalColetaMaterialOut(LocalColetaMaterialBase):
    id: int
    dataCadastro: datetime

    class Config:
        from_attributes = True
        
# Schemas para tabela Materiais
class MaterialBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    pontos: float

class MaterialCreate(MaterialBase):
    pass

class MaterialOut(MaterialBase):
    id: int
    dataCadastro: datetime

    class Config:
        from_attributes = True
        
# Schemas para tabela tipo_usuario
class TipoUsuarioBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class TipoUsuarioCreate(TipoUsuarioBase):
    pass

class TipoUsuarioOut(TipoUsuarioBase):
    id: int

    class Config:
        from_attributes = True