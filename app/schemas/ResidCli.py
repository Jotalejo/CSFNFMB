from pydantic import BaseModel

# Todas las propiedades que tiene un cliente en la base de datos, sin el id
class ResidCliBase(BaseModel):
    ccliente : int | None = None
    cresiduo : int | None = None
    cantresiduo : float | None = None
    pesopromres : float | None = None
    segregares : str | None = None
    numbolsas : int | None = None
    observaciones : str | None = None
    # Definimos el método from_dict para crear una instancia de ResidCliBase a partir de un diccionario

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

# Clase para crear un Residuo del cliente 
class ResCliCreate(ResidCliBase):
    pass

# Residuo del Cliente completo para la respuesta
class ResCliClass(ResidCliBase):
    id : int


