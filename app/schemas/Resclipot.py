# schemas/Resclipot.py
from pydantic import BaseModel
from typing import Optional


class ResiduosCliBase(BaseModel):
    codcli: int
    tresiduo: int
    cantresiduo: Optional[float] = None
    pesopromres: Optional[float] = None
    segregares: Optional[str] = None
    numbolsas: Optional[int] = None
    observaciones: Optional[str] = None


class ResiduosCliCreate(ResiduosCliBase):
    pass


class ResiduosCliUpdate(BaseModel):
    id: int
    codcli: Optional[int] = None
    tresiduo: Optional[int] = None
    cantresiduo: Optional[float] = None
    pesopromres: Optional[float] = None
    segregares: Optional[str] = None
    numbolsas: Optional[int] = None
    observaciones: Optional[str] = None


class ResiduosCliOut(ResiduosCliBase):
    id: int

    class Config:
        from_attributes = True   # (Pydantic v2) -> orm_mode=True si usas v1
