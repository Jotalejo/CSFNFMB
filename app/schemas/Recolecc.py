from pydantic import BaseModel

# Todas las propiedades que tiene un cliente en la base de datos, sin el id
class RecoleccBase(BaseModel):
    cliente : int | None = None 
    fecha : Date | None = None 
    hora : Time | None = None 
    tresiduo : int | None = None
    cantresiduo : int | None = None
    peso : Float | None = None
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


