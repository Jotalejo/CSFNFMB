# schemas/Citas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class CitaBase(BaseModel):
    clipot: Optional[int] = None
    fechacita: Optional[date] = None
    horacita: Optional[time] = None
    cliente: Optional[int] = None
    asuntocita: Optional[str] = None
    tipodevisi: Optional[int] = None
    iniciocita: Optional[time] = None
    fincita: Optional[time] = None
    actpendcita: Optional[str] = None
    seguiapcita: Optional[date] = None
    actrealcita: Optional[str] = None
    compromcita: Optional[str] = None
    fecompromcita: Optional[date] = None
    lugarcita: Optional[str] = None
    ubiccita: Optional[str] = None
    tipogen: Optional[int] = None
    ciudad: Optional[int] = None
    regioncita: Optional[str] = None
    observaciones: Optional[str] = None

    @classmethod
    def from_dictC(cls, data: dict):
        return cls(**data)

class CitaCreate(CitaBase):
    pass

class Cita(CitaBase):
    id: int
    class Config:
        from_attributes = True   # (Pydantic v2). Si usas v1: orm_mode = True
