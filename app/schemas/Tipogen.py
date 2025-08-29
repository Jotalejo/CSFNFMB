from pydantic import BaseModel

# Todas las propiedades que tiene Tipogen en la base de datos, sin el id
class TipoGen(BaseModel):
    nombre : str | None = None
    tamax : int | None = None 
    tamin : int | None = None 
    observaciones : str | None = None 
    
    @classmethod
    def from_dictTipL(cls, data: dict):
        return cls(**data)