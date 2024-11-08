from pydantic import BaseModel

class ClienteBase(BaseModel):
    razonSocial : str
    nit : str | None = None


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id : int
