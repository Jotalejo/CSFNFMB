from pydantic import BaseModel

# Todas las propiedades que tiene Logistica en la base de datos, sin el id
class Logispot(BaseModel):
    codclipot : int | None = None 
    frecuerec : str | None = None
    capavehic : str | None = None
    distancia : float | None = None 
    observaciones : str | None = None 
    
    @classmethod
    def from_dictLogp(cls, data: dict):
        return cls(**data)

# Clase para crear una Logistica potencial 
class LogiPotCreate(Logispot):
    pass