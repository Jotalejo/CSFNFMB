from pydantic import BaseModel, conint, confloat
from datetime import date, time
from typing import List, Optional


class ResiduoItem(BaseModel):
    tresiduo: int
    cantidad: int
    peso: float
    peso_total: Optional[float] = None
    fecha: date | None = None              # fecha_recolec
    hora: time | None = None

# Todas las propiedades que tiene un cliente en la base de datos, sin el id


class RecoleccBase(BaseModel):
    # ⬇️ Nombres EXACTOS como en tu Model
    cliente_id: int | None = None             # codcli_recolec
    fecha: date | None = None              # fecha_recolec
    hora: time | None = None               # hora_recolec
    tresiduo: int | None = None            # codtipores_recolec
    cantresiduo: int | None = None         # cantidbolsas_recolec
    peso: float | None = None              # pesotot_recolec
    estado: int | None = None           # codest_recolec
    vehiculo: int | None = None            # codveh_recolec
    codigobar: str | None = None
    firmarecolec: str | None = None
    lafirmaderecibo: Optional[str] = None   # ⬅️ nuevo
    observaciones: str | None = None
    # ⬅️ nuevo para lista de residuos
    residuos: Optional[List[ResiduoItem]] = None
    direccion: str | None = None
    telefono: str | None = None
    ciudad: str | None = None
    email: str | None = None
    contacto: str | None = None
    telefono_contacto: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

# Clase para crear una recolección


class RecolectCreate(RecoleccBase):
    pass

# Recolección completo para la respuesta


class Recolecc(RecoleccBase):
    id: int

# Clase para la respuesta de una recolección


class RecoleccOut(RecoleccBase):
    id: int

    class Config:
        from_attributes = True
