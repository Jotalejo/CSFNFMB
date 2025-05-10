from pydantic import BaseModel

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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

# Clase para crear un cliente 
class ClienteCreate(ClienteBase):
    pass

# Cliente completo para la respuesta
class Cliente(ClienteBase):
    id : int


