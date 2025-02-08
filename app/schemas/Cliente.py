from pydantic import BaseModel

class ClienteBase(BaseModel):
    razonSocial : str
    nit : str | None = None
    direccion : str | None = None 
    telefono : str | None = None 
    ciudad : str | None = None 
    actividad : str | None = None 
    contacto : str | None = None 
    telefonoContacto : str | None = None 
    observaciones : str | None = None 

class ClienteCreate(ClienteBase):

    pass


class Cliente(ClienteBase):
    id : int
