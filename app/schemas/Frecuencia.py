# schemas/Frecuencia.py
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import time

TipoNombre = Literal["diaria", "semanal", "mensual"]

class FrecuenciaBase(BaseModel):
    cliente_id: int
    tipo_nombre: TipoNombre            # diaria|semanal|mensual
    dias_semana: Optional[List[int]] = None  # 1..7 (L..D) para semanal/diaria
    dias_mes: Optional[str] = None           # "1,10,20,30" para mensual
    hora_desde: Optional[time] = None
    hora_hasta: Optional[time] = None
    veces: Optional[int] = None
    capacidad_kg: Optional[int] = Field(None, ge=1, le=1000)
    observ: Optional[str] = None
    activo: Optional[bool] = True

class FrecuenciaCreate(FrecuenciaBase):
    pass

class FrecuenciaOut(FrecuenciaBase):
    id: int
    tipo_id: int

    class Config:
        from_attributes = True
