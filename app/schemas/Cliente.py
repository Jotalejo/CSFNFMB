from pydantic import BaseModel
from typing import Optional

# Todas las propiedades que tiene un cliente en la base de datos, sin el id
class ClienteBase(BaseModel):
    razonSocial : str
    nit : str | None = None
    direccion : str | None = None 
    telefono : str | None = None 
    ciudad : int | None = None 
    contacto : str | None = None 
    telefonoContacto : str | None = None 
    observaciones : str | None = None 
    email: str | None = None

# nuevos campos de geolocalización
    latrecolec: Optional[float] = None    # mapea a latrecolec_cli
    lngrecolec: Optional[float] = None    # mapea a lngrecolec_cli
    linkmaps: Optional[str] = None        # mapea a linkmaps_cli

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    class Config:
        orm_mode = True            # Pydantic v1
        from_attributes = True   # si estás en v2

# Clase para crear un cliente 
class ClienteCreate(ClienteBase):
    pass

# Cliente completo para la respuesta
class Cliente(ClienteBase):
    id : int


