from pydantic import BaseModel

# Todas las propiedades que tiene TipoVisita en la base de datos, sin el id
class TipoGen(BaseModel):
    nombre : str | None = None
    observaciones : str | None = None 
    
    @classmethod
    def from_dictTipVis(cls, data: dict):
        return cls(**data)