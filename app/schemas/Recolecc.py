from pydantic import BaseModel
from datetime import date, time

# Todas las propiedades que tiene un cliente en la base de datos, sin el id
class RecoleccBase(BaseModel):
    cliente : int | None = None 
    fecha : date | None = None 
    hora : time | None = None 
    tresiduo : int | None = None
    cantresiduo : int | None = None
    peso : float | None = None
    estado : int | None = None
    vehiculo : int | None = None
    codigobar : str | None = None
    firmarecolec : str | None = None
    observaciones : str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

# Clase para crear una recolección 
class RecolectCreate(RecoleccBase):
    pass

# Recolección completo para la respuesta
class Recolecc(RecoleccBase):
    id : int


