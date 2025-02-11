from pydantic import BaseModel

class ClienteBase(BaseModel):
    razonSocial : str
    nit : str | None = None
    direccion : str | None = None 
    telefono : str | None = None 
    ciudad : str | None = None 
    contacto : str | None = None 
    telefonoContacto : str | None = None 
    observaciones : str | None = None 
    email: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id : int


