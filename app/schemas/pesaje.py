from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class DetallePesajeItem(BaseModel):
    detalle_recoleccion_id: int | None = None
    tipo_residuo_id: int | None = None
    bolsas: int | None = None
    peso: float | None = None
    confirmado: int | None = 0
    observaciones: str | None = None


class PesajeBase(BaseModel):
    recoleccion_id: int | None = None
    vehiculo_id: int | None = None
    cliente_id: int | None = None
    fecha: date | None = None
    estado: str | None = "PENDIENTE"
    firma_verificacion: str | None = None
    observaciones: str | None = None

    detalles: Optional[List[DetallePesajeItem]] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class PesajeCreate(PesajeBase):
    pass


class PesajeOut(PesajeBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class DetallePesajeOut(DetallePesajeItem):
    id: int
    pesaje_id: int | None = None

    class Config:
        from_attributes = True