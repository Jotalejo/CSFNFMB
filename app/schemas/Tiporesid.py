# schemas/TipoResid.py
from pydantic import BaseModel
from typing import Optional

class TipoResidBase(BaseModel):
    nombre: Optional[str] = None
    codsubclres: Optional[int] = None
    observaciones: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class TipoResidCreate(TipoResidBase):
    pass

class TipoResidOut(TipoResidBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 (si usas v1 -> orm_mode = True)
