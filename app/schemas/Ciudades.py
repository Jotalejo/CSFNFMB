from pydantic import BaseModel

class CiudadBase(BaseModel):
    codigo : str
    nombre : str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class Ciudad(CiudadBase):
    id : int


