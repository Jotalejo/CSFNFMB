# schemas/transporte.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, time

class PlanParada(BaseModel):
    recoleccion_id: Optional[int] = None
    cliente_id: int
    cliente_nombre: str
    direccion: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    hora_pref: Optional[time] = None
    ventana_ini: Optional[time] = None
    ventana_fin: Optional[time] = None
    capacidad_kg: Optional[int] = None
    orden: Optional[int] = None

class PlanVehiculo(BaseModel):
    vehiculo: Optional[dict] = None  # {"id":int,"placa":str,"capacidad":int}
    paradas: List[PlanParada] = Field(default_factory=list)

class PlanResponse(BaseModel):
    plan: List[PlanVehiculo] = Field(default_factory=list)

class GuardarPlanRequest(BaseModel):
    fecha: date
    plan: List[PlanVehiculo]
